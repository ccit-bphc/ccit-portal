"""
Custom Adapter For Things.
"""

from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Custom Adapter for checking email domain before login."""

    def pre_social_login(self, request, sociallogin):
        u = sociallogin.user
        if u.email.split("@")[1] not in settings.ALLOWED_DOMAINS:
            messages.error(
                request, "Please login through bits-mail or contact the administrator."
            )
            raise ImmediateHttpResponse(render(request, "registration/login.html"))
