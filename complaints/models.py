from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="complainer")
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField()
    remark = models.TextField()
    remark_to_user = models.TextField()
    urgency = models.BooleanField(default=False)
    urgency_reason = models.TextField()
    handler = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="handler"
    )

    def __str__(self):
        return f"{self.user} - {self.category} - {self.id}"
