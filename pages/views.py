from users.permissions import user_is_logged_in_and_active
from django.shortcuts import render, redirect


@user_is_logged_in_and_active
def home(request):
    if not request.user.is_authenticated:
        return redirect("account-login")

    return render(
        request, "complaints/complaints_register.html"
    )


def contact(request):
    return render(
        request, "registration/contact.html"
    )


def denied(request):
    return render(request, "registration/denied.html")
