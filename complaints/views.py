"""Module for creating views to manage user complaints"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from users.permissions import (
    user_is_logged_in_and_active,
    user_is_staff,
    user_is_nucleus,
    user_is_staff_or_nucleus,
)
from .models import Complaint, UnblockRequest
from .forms import ComplaintForm, UnblockRequestForm


@user_is_logged_in_and_active
def previous(request):
    """View for displaying previous complaints of the user"""
    user = request.user
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
    complaint = Complaint.objects.get(request.POST.get("id"))
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
    unblock = UnblockRequest.objects.get(request.POST.get("id"))
    if unblock.user != user:
        return redirect("previous-requests")
    unblock.delete()
    messages.success(request, "Your Request has been Successfully Cancelled.")
    return redirect("previous-requests")


@user_is_logged_in_and_active
def register_complaint(request):
    if request.method == "POST":
        form = ComplaintForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.user = request.user
            form_obj.save()
            email_on_request(
                request_id=form_obj.id,
                category=form_obj.category,
                details=form_obj.remark,
                issue="Complaint",
                user_email=request.user.email,
            )

            messages.success(request, "Your Complaint has been Successfully Registered")
            return render(request, "registration/home.html", context={"title": "home"})
    else:
        form = ComplaintForm()
        return render(request, "complaints/complaints_register.html", {"form": form})


@user_is_logged_in_and_active
@user_is_staff_or_nucleus
def handle_complaint(request):
    if request.method == "POST":
        complaint_id = request.POST.get("id")
        complaint_set = Complaint.objects.filter(id=complaint_id)
        complaint_obj = complaint_set[0]
        complaint_obj.status = request.POST.get("status")
        complaint_obj.handler = request.user
        complaint_obj.remark_to_user = request.POST.get("remark_to_user")
        complaint_obj.resolved_at = timezone.now()
        complaint_obj.save()
        if complaint_obj.status == Complaint.TAKEN_UP:
            complaint_obj.status = "Taken up by a technician"
        email_resolve(
            category=complaint_obj.category,
            request_id=complaint_obj.id,
            issue="Complaint",
            user_email=request.user.email,
            request_status=complaint_obj.status,
            details=complaint_obj.remark,
            remark_user=complaint_obj.remark_to_user,
        )
        return render(
            request, "complaints/previous_complaints.html", context={"title": "home"}
        )


@user_is_logged_in_and_active
@user_is_staff_or_nucleus
def display_to_staff(request):
    """View to display the pending requests and complaints to staff members"""
    complaints = Complaint.objects.filter(status=Complaint.REGISTERED).order_by(
        "-uploaded_at"
    )
    requests = UnblockRequest.objects.filter(status=UnblockRequest.REGISTERED).order_by(
        "-uploaded_at"
    )
    requests_verified = UnblockRequest.objects.filter(
        status=UnblockRequest.VERIFIED
    ).order_by("-uploaded_at")
    complaints_handled = Complaint.objects.filter(
        handler=request.user, status=Complaint.TAKEN_UP
    ).order_by("-uploaded_at")
    return render(
        request,
        "complaints/handle_requests.html",
        context={
            "complaints_handler": complaints_handled,
            "complaints": complaints,
            "requests": requests,
            "requests_verified": requests_verified,
        },
    )


@user_is_logged_in_and_active
def request_unblock(request):
    """View For Registering Request for unblocking websites"""
    if request.method == "POST":
        form = UnblockRequestForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.user = request.user
            form_obj.save()
            email_on_request(
                request_id=form_obj.id,
                category="Request to Unblock Website",
                details=form_obj.reason,
                issue="Request",
                user_email=request.user.email,
            )
            messages.success(request, "Your Request has been Successfully Registered")
            return render(request, "registration/home.html", context={"title": "home"})


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
        request_obj.remark_to_user = request.POST.get("remark_to_user")
        request_obj.resolved_at = timezone.now()
        request_obj.save()
        if request_obj.status == UnblockRequest.VERIFIED:
            email_verified(url=request_obj.url)
        else:
            email_resolve(
                category=request_obj.category,
                request_id=request_obj.id,
                issue="Request",
                user_email=request.user.email,
                request_status=request_obj.status,
                details=request_obj.remark,
                remark_user=request_obj.remark_to_user,
            )
        return render(
            request, "complaints/previous_complaints.html", context={"title": "home"}
        )


def email_on_request(request_id, category, details, issue, user_email):
    """Function to send email to the user and staff when he registers a new complaint or request"""

    from_email = settings.EMAIL_HOST_USER
    subject = f"{issue} Registered"
    message = (
        f"Your {issue} with reference number {request_id}, "
        f"category- {category} and details- {details} has been successfully registered. "
        f"Soon a technician will be alloted to look into the issue"
    )
    to_email = [user_email]
    send_mail(subject, message, from_email, to_email, fail_silently=True)
    subject = f"New {issue} Registered"
    message = (
        f"New {issue} with reference id {request_id}, "
        f"category- {category} and details- {details} has been registered. "
        f"Please allocate a technician to look into the issue"
    )
    to_email = ["ccit_student_nucleus@hyderabad.bits-pilani.ac.in"]
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
    to_email = ["ccit@hyderabad.bits-pilani.ac.in"]
    send_mail(subject, message, from_email, to_email, fail_silently=True)
