"""
Custom Adapter For Things.
"""

from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import get_adapter as get_account_adapter


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Custom Adapter for checking email domain before login."""

    def pre_social_login(self, request, sociallogin):
        user_obj = sociallogin.user
        user_obj.username = user_obj.email.split("@")[0]
        if user_obj.email.split("@")[1] not in settings.ALLOWED_DOMAINS:
            messages.error(
                request, "Please login through bits-mail or contact the administrator."
            )
            raise ImmediateHttpResponse(redirect("account-login"))

    def save_user(self, request, sociallogin, form=None):
        u = sociallogin.user
        u.set_unusable_password()
        if form:
            get_account_adapter().save_user(request, u, form)
        else:
            get_account_adapter().populate_username(request, u)
        if str.isdigit(u.username[1]):
            if u.username[0] == "f":
                u.category = "FD"
            elif request.user.username[0] == "h":
                u.category = "HD"
            else:
                u.category = "PD"
        else:
            messages.error(request, "Please login using a valid Student Bitsmail")
            raise ImmediateHttpResponse(redirect("account-login"))
        u.enrollment_year = int(u.username[1:5])
        sociallogin.save(request)
        return u

    def authentication_error(
        self, request, provider_id, error=None, exception=None, extra_context=None
    ):
        if not request.user.is_anonymous:
            messages.error(
                request,
                (
                    f"You are already logged in as {request.user.username}. "
                    "Please logout first to login as another user"
                ),
            )
            raise ImmediateHttpResponse(redirect("home"))
        else:
            messages.error(request,"Could not connect to Google Servers.Please Try Again!")
            raise ImmediateHttpResponse(redirect("home"))
