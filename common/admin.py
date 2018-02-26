from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.City)
admin.site.register(models.Subject)
admin.site.register(models.Level)
admin.site.register(models.BaseLevel)