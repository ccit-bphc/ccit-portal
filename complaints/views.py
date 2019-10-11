"""Module for creating views to manage user complaints"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from users.permissions import user_is_logged_in_and_active, user_is_staff_or_nucleus
from .models import Complaint, UnblockRequest
from .forms import ComplaintForm, UnblockRequestForm


@user_is_logged_in_and_active
def previous(request):
    """View for displaying previous complaints and requests of the user"""
    user = request.user
    if user.is_staff or user.is_nucleus:
        return redirect("home")
    complaints = Complaint.objects.filter(user=user).order_by("-uploaded_at")
    unblocks = UnblockRequest.objects.filter(user=user).order_by("-request_time")
    return render(
        request,
        "complaints/previous_requests.html",
        context={"complaints": complaints, "unblocks": unblocks},
    )


@user_is_logged_in_and_active
def cancel_complaint(request):
    """User can cancel their own complaint"""
    if request.method != "POST":
        return redirect("previous-requests")
    user = request.user
    complaint = Complaint.objects.get(pk=request.POST.get("id"))
    if complaint.user != user:
        return redirect("previous-requests")
    complaint.handler = user
    complaint.resolved_at = timezone.now()
    complaint.status = complaint.CANCELLED
    complaint.save()
    messages.success(request, "Your Complaint has been Successfully Cancelled.")
    return redirect("previous-requests")


@user_is_logged_in_and_active
def cancel_unblock_request(request):
    """User can cancel their own unblock request"""
    if request.method != "POST":
        return redirect("previous-requests")
    user = request.user
    unblock = UnblockRequest.objects.get(pk=request.POST.get("id"))
    if unblock.user != user:
        return redirect("previous-requests")
    unblock.delete()
    messages.success(request, "Your Request has been Successfully Cancelled.")
    return redirect("previous-requests")


@user_is_logged_in_and_active
def register_complaint(request):
    if request.method == "POST":
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.user = request.user
            if form_obj.urgency:
                if request.user.category not in settings.PRIVILEGED_USERS:
                    if timezone.now().month > 5:
                        if (timezone.now().year - request.user.enrollment_year) < 3:
                            form_obj.urgency = False
                    else:
                        if (timezone.now().year - request.user.enrollment_year) < 4:
                            form_obj.urgency = False
            try:
                form_obj.save()
                email_on_request(
                    request_id=form_obj.id,
                    category=form_obj.category,
                    details=form_obj.remark,
                    issue="Complaint",
                    user_email=request.user.email,
                )
                if not form_obj.urgency and form_obj.urgency_reason:
                    email_for_verification(
                        request_id=form_obj.id,
                        category=form_obj.category,
                        details=form_obj.remark,
                        issue="Urgent Complaint",
                    )
                request.user.contact_no = form_obj.contact_no
                request.user.save()
                messages.success(
                    request, "Your Complaint has been Successfully Registered"
                )
            except ValidationError as e:
                for err in e:
                    messages.error(request, f"{err} Complaint not registered. Please try again.")

        else:
            messages.error(
                request, "Please fill all the details correctly in the form provided"
            )
    return render(request, "complaints/complaints_register.html")


@user_is_logged_in_and_active
@user_is_staff_or_nucleus
def verify_urgency(request):
    if request.method == "POST":
        comp_id = request.POST.get("id")
        complaint_set = Complaint.objects.filter(id=comp_id)
        complaint_obj = complaint_set[0]
        complaint_obj.urgency = request.POST.get("urgency")
        complaint_obj.handler = request.user
        complaint_obj.save()
    return display_urgent_complaint(request)


@user_is_logged_in_and_active
@user_is_staff_or_nucleus
def display_urgent_complaint(request):
    if request.user.is_nucleus:
        complaints = Complaint.objects.filter(urgency=False).exclude(
            urgency_reason=None
        )
    else:
        complaints = Complaint.objects.filter(urgency=True)
    context = {"complaints": complaints}
    return render(request, "complaints/urgent_complaints.html", context)


@user_is_logged_in_and_active
@user_is_staff_or_nucleus
def handle_complaint(request):
    if request.method == "POST":
        complaint_id = request.POST.get("id")
        complaint_set = Complaint.objects.filter(id=complaint_id)
        complaint_obj = complaint_set[0]
        complaint_obj.status = request.POST.get("status")
        complaint_obj.handler = request.user
        complaint_obj.remark_to_user = request.POST.get("remark_to_user", None)
        complaint_obj.resolved_at = timezone.now()
        complaint_obj.save()
        if complaint_obj.status == Complaint.TAKEN_UP:
            request_status = "Taken Up"
        if complaint_obj.status == Complaint.DONE:
            request_status = "Resolved"
        email_resolve(
            category=complaint_obj.category,
            request_id=complaint_obj.id,
            issue="Complaint",
            user_email=complaint_obj.user.email,
            request_status=request_status,
            details=complaint_obj.remark,
            remark_user=complaint_obj.remark_to_user,
        )
    return display_complaint(request)


@user_is_logged_in_and_active
@user_is_staff_or_nucleus
def display_complaint(request):
    """View to display the pending requests and complaints to staff members"""
    if request.user.is_staff:
        complaints_list = (
            Complaint.objects.filter(
                Q(status=Complaint.REGISTERED)
                | Q(handler=request.user, status=Complaint.TAKEN_UP)
            )
            .exclude(urgency=True)
            .order_by("-uploaded_at")
        )
    if request.user.is_nucleus:
        complaints_list = (
            Complaint.objects.filter(
                Q(status=Complaint.REGISTERED) | Q(status=Complaint.TAKEN_UP)
            )
            .exclude(urgency=True)
            .order_by("-uploaded_at")
        )

    page = request.GET.get("page", 1)

    paginator = Paginator(complaints_list, 2)
    try:
        complaints = paginator.page(page)
    except PageNotAnInteger:
        complaints = paginator.page(1)
    except EmptyPage:
        complaints = paginator.page(paginator.num_pages)
    return render(
        request, "complaints/handle_complaints.html", context={"disp_list": complaints}
    )


@user_is_logged_in_and_active
@user_is_staff_or_nucleus
def display_request(request):
    if request.user.is_nucleus:
        requests_list = UnblockRequest.objects.filter(
            status=UnblockRequest.REGISTERED
        ).order_by("-request_time")
    else:
        requests_list = UnblockRequest.objects.filter(
            status=UnblockRequest.VERIFIED
        ).order_by("-request_time")

    page = request.GET.get("page", 1)

    paginator = Paginator(requests_list, 10)
    try:
        requests = paginator.page(page)
    except PageNotAnInteger:
        requests = paginator.page(1)
    except EmptyPage:
        requests = paginator.page(paginator.num_pages)

    return render(
        request, "complaints/handle_requests.html", context={"disp_list": requests}
    )


@user_is_logged_in_and_active
def request_unblock(request):
    """View For Registering Request for unblocking websites"""
    if request.method == "POST":
        form = UnblockRequestForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.user = request.user
            try:
                form_obj.save()
                email_on_request(
                    request_id=form_obj.id,
                    category="Request to Unblock Website",
                    details=form_obj.reason,
                    issue="Request",
                    user_email=request.user.email,
                )
                email_for_verification(
                    request_id=form_obj.id,
                    category="Request to Unblock Website",
                    details=form_obj.reason,
                    issue="URL Unblock Request",
                )
                messages.success(
                    request, "Your Request has been Successfully Registered"
                )
            except ValidationError as e:
                if str(e) == "['Given Url is under consideration.']":
                    messages.success(
                        request,
                        "This url is under consideration. The issue will soon be resolved.",
                    )
                    return render(request, "complaints/request_unblock.html")
                if str(e) == "['Given Url is already unblocked.']":
                    messages.success(request, "This url has already been unblocked.")
                    return render(request, "complaints/request_unblock.html")
                else:
                    messages.error(request, "Please fill up form correctly.")
                    return render(request, "complaints/request_unblock.html")
        else:
            messages.error(
                request, "Please fill all the details correctly in the form provided"
            )
        return render(request, "complaints/request_unblock.html")
    user = request.user
    complaints = Complaint.objects.filter(user=user).order_by("-uploaded_at")
    unblocks = UnblockRequest.objects.filter(user=user).order_by("-request_time")
    return render(
        request,
        "complaints/request_unblock.html",
        context={"complaints": complaints, "unblocks": unblocks},
    )


@user_is_logged_in_and_active
@user_is_staff_or_nucleus
def handle_unblock_request(request):
    """View For Handling Request for unblocking websites"""
    if request.method == "POST":
        user_id = request.POST.get("id")
        request_set = UnblockRequest.objects.filter(id=user_id)
        request_obj = request_set[0]
        request_obj.status = request.POST.get("status")
        request_obj.handler = request.user
        request_obj.remark_to_user = request.POST.get("remark_to_user", None)
        request_obj.resolved_at = timezone.now()
        request_obj.save()
        if request_obj.status == UnblockRequest.VERIFIED:
            email_verified(url=request_obj.url)
        else:
            if request_obj.status == UnblockRequest.CANCELLED:
                request_status = "Cancelled"
            else:
                request_status = "Resolved"
            email_resolve(
                category="URL Unblock Request",
                request_id=request_obj.id,
                issue="Request",
                user_email=request_obj.user.email,
                request_status=request_status,
                details=request_obj.url,
                remark_user=request_obj.remark_to_user,
            )
    return display_request(request)


def email_on_request(request_id, category, details, issue, user_email):
    """Function to send email to the user and staff when he registers a new complaint or request"""

    from_email = settings.EMAIL_HOST_USER
    subject = f"{issue} Registered"
    message = (
        f"Your {issue} with reference ID- {request_id}, "
        f"category- {category} and details- {details} ,has been successfully registered. "
        f"Soon a technician will be alloted to look into the issue"
    )
    to_email = [user_email]
    send_mail(subject, message, from_email, to_email, fail_silently=True)
    if issue == "Complaint":
        subject = f"New {issue} Registered"
        message = (
            f"New {issue} with reference ID {request_id}, "
            f"category- {category} and details- {details} ,has been registered. "
            f"Please allocate a technician to look into the issue"
        )
        to_email = [settings.ADMIN_EMAIL]
        send_mail(subject, message, from_email, to_email, fail_silently=True)


def email_resolve(
    request_id, request_status, issue, user_email, category, details, remark_user
):
    """Function to send email to the user when his request or compliant gets resolved"""
    subject = f"{issue} {request_status}"
    message = (
        f"Your {issue} with reference number {request_id}, "
        f"category- {category} and details- {details} has been {request_status}. "
        f"Remark- {remark_user}. Contact the adminstrator for further queries."
    )
    from_email = settings.EMAIL_HOST_USER
    to_email = [user_email]
    send_mail(subject, message, from_email, to_email, fail_silently=True)


def email_verified(url):
    """Function to send email to ccit when the ccit nucleus verifies an unblock request"""
    subject = "Website Unblock Request Verified"
    message = (
        "CCIT Student Nucleus has verified the request for unblocking "
        f"the website- {url} to be genuine. "
        "Please do the needful at the earliest."
    )
    from_email = settings.EMAIL_HOST_USER
    to_email = [settings.ADMIN_EMAIL]
    send_mail(subject, message, from_email, to_email, fail_silently=True)


def email_for_verification(issue, request_id, category, details):
    """Function to send email to ccit nucleus when a
        new unblock request is received or an unprivileged user
        registers an urgent complaint"""
    subject = f"Verify {issue}"
    message = (
        f"A new {issue} with reference number {request_id}, "
        f"category- {category} and details- {details} has been registered. "
        f"Please Verify it so that ccit staff can take necessary action over it."
    )
    from_email = settings.EMAIL_HOST_USER
    to_email = [settings.CCIT_NUCLEUS_EMAIL]
    send_mail(subject, message, from_email, to_email, fail_silently=True)
