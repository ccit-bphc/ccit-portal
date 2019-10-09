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
            "bhavan",
            "contact_no",
            "room_no",
            "avail_start_time",
            "avail_end_time",
            "avail_date",
            "image",
        )


class UnblockRequestForm(forms.ModelForm):
    """Model Form for handling requests for unblocking websites"""

    class Meta:
        model = models.UnblockRequest
        fields = ("url", "reason")
