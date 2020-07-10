from django.contrib import admin

from . import models
# registering the models
admin.site.register(models.Rider)
admin.site.register(models.Driver)
admin.site.register(models.Request)
admin.site.register(models.Ride)
