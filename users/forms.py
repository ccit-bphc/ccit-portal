"""
Forms related to user registration and login.
"""

from django.conf import settings
from django import forms
from allauth.socialaccount.forms import SignupForm


class CustomSignupForm(SignupForm):
    def clean_email(self):
        email = self.cleaned_data["email"]
        if email.split("@")[1].lower() not in settings.ALLOWED_DOMAINS:
            raise forms.ValidationError(
                "Your account is not registered with BITS Pilani, Hyderabad Campus. "
                "If you think this is a problem, then please contact the administrator."
            )
        return email
