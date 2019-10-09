"""Module for Creating Complaints Model"""
from datetime import date, time, timedelta, datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from tld import get_fld
from tld.exceptions import TldBadUrl, TldDomainNotFound


class Complaint(models.Model):
    """Model Class for storing complaint tickets"""

    PHONE_REGEX = r"^(\+?91[\-\s]?)?[0]?(91)?[789]\d{9}$"
    GIRLS_TIME_LIMITS = [(time(16, 30), time(17)), (time(12), time(13, 30))]
    TECHNICIAN_WORK_HOURS = [(time(9), time(13)), (time(14), time(17))]

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

    KRISHNA = "K"
    RAM = "R"
    SHANKAR = "S"
    GANDHI = "G"
    BUDH = "B"
    VYAS = "V"
    GAUTAM = "GT"
    VALMIKI = "VM"
    MEERA = "M"
    MALVIYA = "MM"
    VK_BOYS = "VB"
    VK_GIRLS = "VG"
    MRS_TOWER = "MR"
    H8_BLOCK = "H8"

    BHAVAN_CHOICES = (
        (None, "Bhavan"),
        (KRISHNA, "Krishna"),
        (RAM, "Ram"),
        (SHANKAR, "Shankar"),
        (GANDHI, "Gandhi"),
        (BUDH, "Budh"),
        (VYAS, "Vyas"),
        (GAUTAM, "Gautam"),
        (VALMIKI, "Valmiki"),
        (MEERA, "Meera"),
        (MALVIYA, "Malviya"),
        (VK_BOYS, "Vishwakarma Boys"),
        (VK_GIRLS, "Vishwakarma Girls"),
        (MRS_TOWER, "MRS Tower"),
        (H8_BLOCK, "H8 Block"),
    )

    GIRLS_BHAVANS = (MEERA, MALVIYA, VK_GIRLS)

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
    bhavan = models.CharField(max_length=2, choices=BHAVAN_CHOICES)
    room_no = models.PositiveIntegerField(null=False, blank=False)
    avail_start_time = models.TimeField(null=False, blank=False)
    avail_end_time = models.TimeField(null=False, blank=False)
    avail_date = models.DateField(null=False, blank=False)
    handler = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="handler"
    )
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.category} - {self.id}"

    def save(self, *args, **kwargs):
        self.validate_timings(self.avail_start_time, self.avail_end_time)
        if self.status == self.REGISTERED:
            self.validate_date(self.avail_date)
        self.validate_urgency(self.urgency, self.urgency_reason)
        self.validate_handler(self.user, self.handler, self.status)
        super().save(*args, **kwargs)

    def validate_timings(self, avail_start_time, avail_end_time):
        """
        Validate that available timings are in given time slots, if in girls' hostels
        or that is has at least 1 hr of time
        """
        if self.bhavan in self.GIRLS_BHAVANS:
            for start_time, end_time in self.GIRLS_TIME_LIMITS:
                if avail_start_time >= start_time and avail_end_time <= end_time:
                    return
            else:
                raise ValidationError(
                    "Girls' Hostel is only open for limited time slots. Your given time does not fit in them"
                )
        ## Technicians' break time is currently being ignored. If the specifications change, this will need to change
        if avail_start_time < time(9) or avail_end_time > time(17):
            raise ValidationError("Availble time not in technicians' working hours")
        if self.avail_date == date.today():
            if avail_start_time < datetime.now().time():
                raise ValidationError("Available time before complaint registration.")
        if avail_end_time < time(
            avail_start_time.hour + 1, avail_start_time.minute, avail_start_time.second
        ):
            raise ValidationError("Available time is less than one hour.")

    def validate_date(self, avail_date):
        """
        Validate the the available date is in the future and within a week of complaint
        Also make sure that it on a weekday
        """
        if avail_date.weekday() in (5, 6):
            raise ValidationError("Sundays and Saturdays are holidays.")
        if avail_date < date.today() or avail_date > timedelta(days=7) + date.today():
            raise ValidationError("Given date is out of range.")

    def validate_urgency(self, urgency, reason):
        """Validate that an urgent request has an urgency reason"""
        if urgency:
            if reason is None or reason == "":
                raise ValidationError("No urgency reason given for urgent complaint.")

    def validate_handler(self, user, handler, status):
        """Validate that a complaint is handled either by staff or by user"""
        if status == self.REGISTERED:
            if not (handler is None or handler.is_nucleus):
                raise ValidationError("Handler is invalid for given status")
        if status == self.CANCELLED:
            if handler != user:
                raise ValidationError("Complaint Cancellation can only be done by user")
        if status == self.TAKEN_UP:
            if not handler.is_staff:
                raise ValidationError("Only staff members can take up complaints")
        if status == self.DONE:
            if not (handler.is_staff or handler.is_nucleus):
                raise ValidationError("Given handler is not authorised for resolution")


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
        if self.status == self.REGISTERED:
            if self.domain in (
                req.domain
                for req in UnblockRequest.objects.filter(status=UnblockRequest.VERIFIED)
            ):
                raise ValidationError("Given Url is under consideration.")
            if self.domain in (
                req.domain
                for req in UnblockRequest.objects.filter(status=UnblockRequest.DONE)
            ):
                raise ValidationError("Given Url is already unblocked.")
        if self.handler == self.user:
            if self.status != self.CANCELLED:
                raise ValidationError(
                    "User cancelled request but status is not set to cancelled."
                )
        if self.handler and self.handler.is_staff:
            if self.status == self.REGISTERED:
                raise ValidationError("Request handled but status not updated.")
        if not (
            self.handler is None
            or self.handler.is_staff
            or self.handler == self.user
            or self.handler.is_nucleus
        ):
            raise ValidationError("Invalid request handler.")
        if not self.reason:
            raise ValidationError("No reason given for request.")
        super().save(*args, **kwargs)
