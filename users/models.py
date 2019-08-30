from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    PHONE_REGEX = r"^(\+?91[\-\s]?)?[0]?(91)?[789]\d{9}$"
    phone_number_validator = RegexValidator(
        regex=PHONE_REGEX, message="Phone number is not in the correct format."
    )
    contact_no = models.CharField(
        max_length=15, validators=[phone_number_validator], null=True, blank=True
    )
