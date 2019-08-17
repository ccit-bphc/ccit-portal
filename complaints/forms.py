from django import forms
from . import models


class Complaint_form(forms.ModelForm):
    class Meta:
        model=models.Complaint
        fields = ("category", "remark", "urgency", "urgency_reason")


class OpenSite_form(forms.ModelForm):
    class Meta:
        model = models.Complaint
        fields = ("category", "remark")

