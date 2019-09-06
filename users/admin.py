from django.contrib import admin
<<<<<<< HEAD
from . import models
# Register your models here.

admin.site.register(models.CustomUser)
=======
from django.contrib.auth.admin import UserAdmin
from . import models

admin.site.register(models.CustomUser, UserAdmin)
>>>>>>> 76f2c2e3362166a0630b3322a88dcb956c99a72b
