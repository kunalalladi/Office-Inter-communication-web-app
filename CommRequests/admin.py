from django.contrib import admin
from .models import Requests, Labs, LabsAdmin

admin.site.register(Requests)
admin.site.register(Labs, LabsAdmin)

