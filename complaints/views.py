"""Module for creating views to manage user complaints"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from users.permissions import user_is_logged_in_and_active, user_is_staff
from .models import Complaint, UnblockRequest
from .forms import (
    ComplaintForm,
    ComplaintHandleForm,
    UnblockRequestForm,
    UnblockHandleForm,
)


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


def cancel_complaint(request, pk: int):
    """User can cancel their own complaint"""
    if request.method != "POST":
        return redirect("previous-requests")
    user = request.user
    complaint = Complaint.objects.get(pk=pk)
    if complaint.user != user:
        return redirect("previous-requests")
    complaint.handler = user
    complaint.resolved_at = timezone.now()
    complaint.status = complaint.CANCELLED
    complaint.save()
    messages.success(request, "Your Complaint has been Successfully Cancelled.")
    return redirect("previous-requests")


def cancel_unblock_request(request, pk: int):
    """User can cancel their own unblock request"""
    if request.method != "POST":
        return redirect("previous-requests")
    user = request.user
    unblock = UnblockRequest.objects.get(pk=pk)
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
            return render(request, "complaints/complaints_register.html", context={"message": "Complaint Registered Successfully"})
        else:
            return render(request, "complaints/complaints_register.html", context={"message":"Failed"});
    else:
        form = ComplaintForm()
        form2 = UnblockRequestForm()
        return render(request, "complaints/complaints_register.html", {"form": form, "form2": form2, "message":""})


@user_is_logged_in_and_active
@user_is_staff
def handle_complaint(request):
    if request.method == "POST":
        form = ComplaintHandleForm(request.POST)
        print(form);
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.handler = request.user
            form_obj.resolved_at = timezone.now()
            form_obj.save()
            if request.POST.get("status") == Complaint.DONE:
                messages.success(
                    request, "The Complaint has been Successfully Resolved"
                )
                status = "Resolved"
            if request.POST.get("status") == Complaint.CANCELLED:
                messages.success(
                    request, "The Complaint has been Successfully Cancelled"
                )
                status = "Cancelled"
            email_resolve(
                category=form_obj.category,
                request_id=form_obj.id,
                issue="Complaint",
                user_email=request.user.email,
                request_status=status,
                details=form_obj.remark,
                remark_user=form_obj.remark_to_user,
            )
            return render(request, "complaints/previous_complaints.html", context={"title": "home"})


@user_is_logged_in_and_active
@user_is_staff
def display_to_staff(request):
    """View to display the pending requests and complaints to staff members"""
    complaints = Complaint.objects.filter(status=Complaint.REGISTERED).order_by(
        "-uploaded_at"
    )
    requests = UnblockRequest.objects.filter(status=Complaint.REGISTERED).order_by(
        "-uploaded_at"
    )
    return render(
        request,
        "complaints/handle_requests.html",
        context={"complaints": complaints, "requests": requests},
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
            return render(request, "complaints/complaints_register.html", context={"message": "Complaint Registered Successfully"})

@user_is_logged_in_and_active
def handle_unblock_request(request):
    """View For Handling Request for unblocking websites"""

    if request.method == "POST":
        form = UnblockHandleForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.handler = request.user
            form_obj.resolved_at = timezone.now()
            form_obj.save()
            if request.POST.get("status") == Complaint.DONE:
                messages.success(
                    request, "The Complaint has been Successfully Resolved"
                )
                status = "Resolved"
            if request.POST.get("status") == Complaint.CANCELLED:
                messages.success(
                    request, "The Complaint has been Successfully Cancelled"
                )
                status = "Cancelled"
            email_resolve(
                category=form_obj.category,
                request_id=form_obj.id,
                issue="Request",
                user_email=request.user.email,
                request_status=status,
                details=form_obj.reason,
                remark_user=form_obj.remark_to_user,
            )
            return render(request, "registration/home.html", context={"title": "home"})


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
    to_email = ["ccit@hyderabad.bits-pilani.ac.in"]
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
