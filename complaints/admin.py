from django.contrib import admin
from . import models

admin.site.register(models.Complaint)
admin.site.register(models.UnblockRequest)
