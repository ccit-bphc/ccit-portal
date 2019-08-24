"""Module for Creating Complaints Model"""
from datetime import time
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, URLValidator


class Complaint(models.Model):
    """Model Class for storing complaint tickets"""

    REGISTERED = "RD"
    DONE = "DN"
    CANCELLED = "CD"

    STATUS_CHOICES = (
        (REGISTERED, "Registered"),
        (DONE, "Done"),
        (CANCELLED, "Cancelled"),
    )
    CATEGORY_0 = ""
    CATEGORY_1 = "wifi"
    CATEGORY_2 = "lan"
    CATEGORY_3 = "firewall"
    CATEGORY_4 = "url_unblock"

    CATEGORY_CHOICES = (
        (CATEGORY_0, "Choose a Category"),
        (CATEGORY_1, "WiFi"),
        (CATEGORY_2, "Lan"),
        (CATEGORY_3, "Sophos Firewall"),
        (CATEGORY_4, "URL unblock request"),
    )

    PHONE_REGEX = r"^(\+?91[\-\s]?)?[0]?(91)?[789]\d{9}$"

    User = get_user_model()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="complainer")
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default=CATEGORY_0)
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
    room_no = models.CharField(max_length=10,null=False, blank=False)
    avail_start_time = models.TimeField(null=False, blank=False)
    avail_end_time = models.TimeField(null=False, blank=False)
    handler = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="handler"
    )

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
            if self.urgency_reason == "":
                raise ValidationError("No urgency reason given for urgent complaint.")
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

    STATUS_CHOICES = (
        (REGISTERED, "Registered"),
        (DONE, "Done"),
        (CANCELLED, "Cancelled"),
    )

    User = get_user_model()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requestee")
    url_validator = URLValidator(message="This is not a valid URL.")
    url = models.CharField(
		max_length=100,
        validators=[url_validator],
        unique=True,
        error_messages={"unique": "This url is already under consideration"},
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=REGISTERED)
    request_time = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()
    remark_to_user = models.TextField(blank=True, null=True)
    handler = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="resolver", blank=True
    )

    def __str__(self):
        return f"{self.user} - {self.id} - {self.url}"

    def save(self, *args, **kwargs):
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
