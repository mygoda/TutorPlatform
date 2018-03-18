from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.City)
admin.site.register(models.Subject)
admin.site.register(models.Level)
admin.site.register(models.BaseLevel)
admin.site.register(models.TeacherType)
admin.site.register(models.StudentType)
admin.site.register(models.Basis)
admin.site.register(models.Learn)
admin.site.register(models.School)
admin.site.register(models.TeacherRequire)