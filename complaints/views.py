"""Module for creating views to manage user complaints"""
from django.shortcuts import render
from django.contrib import messages
from .models import Complaint
from .forms import ComplaintForm, ComplaintHandleForm


def previous(request):
    """View for displaying previous complaints of the user"""
    if not request.user.is_authenticated:
        return render(request, "registration/home.html", context={"title": "home"})
    user = request.user
    complaints = Complaint.objects.filter(user=user).order_by("-uploaded_at")
    return render(
        request, "complaints/previous_requests.html", context={"complaints": complaints}
    )


def register_complaint(request):
    if not request.user.is_authenticated:
        return render(request, "registration/home.html", context={"title": "home"})

    form = ComplaintForm(request.POST)
    if form.is_valid():
        form_obj = form.save(commit=False)
        form_obj.user = request.user
        form_obj.save()
        messages.success(request, "Your Complaint has been Successfully Registered")
        return render(request, "registration/home.html", context={"title": "home"})
    else:
        form = ComplaintForm()
        return render(request, "complaints/complaints_register.html", {"form": form})


def handle_complaint(request):
    if not request.user.is_authenticated:
        return render(request, "registration/home.html", context={"title": "home"})

    form = ComplaintHandleForm(request.POST)
    if form.is_valid():
        form_obj = form.save(commit=False)
        form_obj.handler = request.user
        form_obj.save()
        if request.POST.get("status") == "DN":
            messages.success(request, "The Complaint has been Successfully Resolved")
        if request.POST.get("status") == "CD":
            messages.success(request, "The Complaint has been Successfully Cancelled")
        return render(request, "registration/home.html", context={"title": "home"})
    else:
        complaints = Complaint.object.filter(status="RD").order_by("-uploaded_at")
        return render(
            request,
            "complaints/handle_requests.html",
            context={"complaints": complaints},
        )


def open_site(request):
    """View For Handling Request for unblocking websites"""
    if request.method == "POST":
        pass
