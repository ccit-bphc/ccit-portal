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
        fields = ("status", "remark_to_user", "resolved_at")


class OpenSiteForm(forms.ModelForm):
    """Model Form for handling requests for unblocking websites"""

    class Meta:
        model = models.Complaint
        fields = ("category", "remark")
