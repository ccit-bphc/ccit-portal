"""Module containing Model forms for receiving and  handling complaints """
from django import forms
from . import models


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = models.Complaint
        fields = (
            "category",
            "remark",
            "urgency",
            "urgency_reason",
            "contact_no",
            "room_no",
            "avail_start_time",
            "avail_end_time",
        )


class ComplaintHandleForm(forms.ModelForm):
    class Meta:
        model = models.Complaint
        fields = ("id", "status", "remark_to_user")


class UnblockRequestForm(forms.ModelForm):
    """Model Form for handling requests for unblocking websites"""

    class Meta:
        model = models.UnblockRequest
        fields = ("url", "reason")


class UnblockHandleForm(forms.ModelForm):
    """Model Form for resolving requests for unblocking websites"""

    class Meta:
        model = models.UnblockRequest
        fields = ("id", "status", "remark_to_user")
