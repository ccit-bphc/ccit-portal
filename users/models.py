from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    CATEGORY_1 = "FD"
    CATEGORY_2 = "HD"
    CATEGORY_3 = "PD"

    CATEGORY_CHOICES = (
        (CATEGORY_1, "First Degree"),
        (CATEGORY_2, "Higer Degree"),
        (CATEGORY_3, "PhD"),
    )
    PHONE_REGEX = r"^(\+?91[\-\s]?)?[0]?(91)?[789]\d{9}$"
    phone_number_validator = RegexValidator(
        regex=PHONE_REGEX, message="Phone number is not in the correct format."
    )
    contact_no = models.CharField(
        max_length=15, validators=[phone_number_validator], null=True, blank=True
    )
    category=models.TextField(choices=CATEGORY_CHOICES, null=True)
    enrollment_year=models.PositiveIntegerField(null=True)

    @property
    def is_nucleus(self):
        return self.groups.filter(name="nucleus").exists()
