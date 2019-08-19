"""Module for Creating Complaints Model"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, validate_email


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

    CATEGORY_1 = "C1"
    CATEGORY_2 = "C2"
    CATEGORY_3 = "C3"
    CATEGORY_4 = "C4"

    CATEGORY_CHOICES = (
        (CATEGORY_1, "CATEGORY_1"),
        (CATEGORY_2, "CATEGORY_2"),
        (CATEGORY_3, "CATEGORY_3"),
        (CATEGORY_4, "CATEGORY_4"),
    )

    PHONE_REGEX = r"^(\+?91[\-\s]?)?[0]?(91)?[789]\d{9}$"

    User = get_user_model()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="complainer")
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=REGISTERED)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField()
    remark = models.TextField()
    remark_to_user = models.TextField()
    urgency = models.BooleanField(default=False)
    urgency_reason = models.TextField()
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
        User, on_delete=models.SET_NULL, null=True, related_name="handler"
    )

    def __str__(self):
        return f"{self.user} - {self.category} - {self.id}"

    def save(self, *args, **kwargs):
        if (self.avail_end_time - self.avail_start_time).total_seconds() < 3600:
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
            self.handler.is_staff or self.handler == self.user or self.handler is None
        ):
            raise ValidationError("Invalid complaint handler.")
        if self.handler.is_staff:
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
    url = models.TextField(
        validators=[validate_email],
        unique=True,
        error_messages={"unique": "This url is already under consideration"},
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=REGISTERED)
    request_time = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()
    remark_to_user = models.TextField()
    handler = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="resolver"
    )

    def __str__(self):
        return f"{self.user} - {self.id} - {self.url}"

    def save(self, *args, **kwargs):
        if self.handler == self.user:
            if self.status != self.CANCELLED:
                raise ValidationError(
                    "User cancelled request but status is not set to cancelled."
                )
        if self.handler.is_staff:
            if self.status == self.REGISTERED:
                raise ValidationError("Request handled but status not updated.")
        if not (
            self.handler.is_staff or self.handler == self.user or self.handler is None
        ):
            raise ValidationError("Invalid request handler.")
        if not self.reason:
            raise ValidationError("No reason given for request.")
        super().save(*args, **kwargs)
