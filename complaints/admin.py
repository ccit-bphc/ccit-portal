from django.contrib import admin
from . import models

admin.site.site_header = 'Computer Centre IT  BITS Pilani,Hyderabad'
admin.site.site_title = 'Administration Page'
admin.site.index_title='CCIT Portal Admin Page'

admin.site.register(models.Complaint)
admin.site.register(models.UnblockRequest)
