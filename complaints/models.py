"""Module for Creating Complaints Model"""
from datetime import time
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from tld import get_fld
from tld.exceptions import TldBadUrl, TldDomainNotFound


class Complaint(models.Model):
    """Model Class for storing complaint tickets"""

    REGISTERED = "RD"
    TAKEN_UP = "TU"
    DONE = "DN"
    CANCELLED = "CD"

    STATUS_CHOICES = (
        (REGISTERED, "Registered"),
        (TAKEN_UP, "Issue Taken Up"),
        (DONE, "Resolved"),
        (CANCELLED, "Cancelled"),
    )

    CATEGORY_1 = "LN"
    CATEGORY_2 = "WF"
    CATEGORY_3 = "SF"

    CATEGORY_CHOICES = (
        (None, "Choose A Category"),
        (CATEGORY_1, "Lan"),
        (CATEGORY_2, "Wifi"),
        (CATEGORY_3, "Sophos Firewall"),
    )

    PHONE_REGEX = r"^(\+?91[\-\s]?)?[0]?(91)?[789]\d{9}$"

    User = get_user_model()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="complainer")
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=REGISTERED)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    remark = models.TextField(null=True, blank=True)
    remark_to_user = models.TextField(null=True, blank=True)
    urgency = models.BooleanField(default=False)
    urgency_reason = models.TextField(null=True, blank=True)
    phone_number_validator = RegexValidator(
        regex=PHONE_REGEX, message="Phone number is not in the correct format."
    )
    contact_no = models.CharField(
        max_length=15, validators=[phone_number_validator], null=False, blank=False
    )
    room_no = models.TextField(null=False, blank=False)
    avail_start_time = models.TimeField(null=False, blank=False)
    avail_end_time = models.TimeField(null=False, blank=False)
    handler = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="handler"
    )
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.category} - {self.id}"

    def save(self, *args, **kwargs):
        if self.avail_end_time < time(
            self.avail_start_time.hour + 1,
            self.avail_start_time.minute,
            self.avail_start_time.second,
        ):
            raise ValidationError("Available time is less than one hour.")
        if self.urgency:
            if self.urgency_reason is None or self.urgency_reason == "":
                raise ValidationError("No urgency reason given for urgent complaint.")
        if not self.user.is_staff:
            if self.handler == self.user:
                if self.status != self.CANCELLED:
                    raise ValidationError(
                        "User cancelled request but status is not set to cancelled."
                    )
        if not (
            self.handler is None or self.handler.is_staff or self.handler == self.user
        ):
            raise ValidationError("Invalid complaint handler.")
        if self.handler and self.handler.is_staff:
            if self.status == self.REGISTERED:
                raise ValidationError("Camplaint handled but status is not updated.")
        super().save(*args, **kwargs)


class UnblockRequest(models.Model):
    REGISTERED = "RD"
    DONE = "DN"
    CANCELLED = "CD"
    VERIFIED = "VF"

    STATUS_CHOICES = (
        (REGISTERED, "Registered"),
        (VERIFIED, "Verified"),
        (DONE, "Done"),
        (CANCELLED, "Cancelled"),
    )

    url_regex = r"^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?"

    User = get_user_model()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requestee")
    url_validator = RegexValidator(regex=url_regex, message="This is not a valid URL.")
    url = models.TextField(validators=[url_validator])
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=REGISTERED)
    request_time = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()
    remark_to_user = models.TextField(blank=True, null=True)
    handler = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="resolver", blank=True
    )
    domain = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.user} - {self.id} - {self.url}"

    def save(self, *args, **kwargs):
        try:
            self.domain = get_fld(self.url)
        except (TldBadUrl, TldDomainNotFound):
            raise ValidationError("Given url is not valid.")
        if self.handler == self.user:
            if self.status != self.CANCELLED:
                raise ValidationError(
                    "User cancelled request but status is not set to cancelled."
                )
        if self.handler and self.handler.is_staff:
            if self.status == self.REGISTERED:
                raise ValidationError("Request handled but status not updated.")
        if not (
            self.handler is None or self.handler.is_staff or self.handler == self.user
        ):
            raise ValidationError("Invalid request handler.")
        if not self.reason:
            raise ValidationError("No reason given for request.")
        super().save(*args, **kwargs)
