from django.contrib import admin

from . import models

admin.site.register(models.Statistics)
admin.site.register(models.Diagnosis)
admin.site.register(models.Schedule)
