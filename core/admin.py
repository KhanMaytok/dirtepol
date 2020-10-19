from django.contrib import admin

from core.models import Vehicle, Asset, RealState

admin.site.register(Asset)
admin.site.register(Vehicle)
admin.site.register(RealState)
