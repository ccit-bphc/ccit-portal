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
        labels = {
            "remark": ("Complaint Details"),
            "contact_no": ("Contact Number"),
            "room_no": ("Room Number"),
            "avail_start_time": ("Complaint Details"),
        }
        widgets = {"contact_no": forms.Textarea(attrs={"cols": 20, "rows": 1})}


class OpenSite_form(forms.ModelForm):
    class Meta:
        model = models.Complaint
        fields = ("category", "remark")

