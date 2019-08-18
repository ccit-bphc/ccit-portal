from django import forms
from . import models


class Complaint_form(forms.ModelForm):
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


class Handle_form(forms.ModelForm):
    class Meta:
        model = models.Complaint
        fields = ("status", "remark_to_user", "resolved_at")


class OpenSite_form(forms.ModelForm):
    class Meta:
        model = models.Complaint
        fields = ("category", "remark")

