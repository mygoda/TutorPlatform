from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Customer)
admin.site.register(models.UserFavorite)
admin.site.register(models.UserRequest)
