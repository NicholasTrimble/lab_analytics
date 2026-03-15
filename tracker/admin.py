from django.contrib import admin
from .models import Doctor, Department, QualityTicket

admin.site.register([Doctor, Department, QualityTicket])