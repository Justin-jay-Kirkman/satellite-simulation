from django.contrib import admin
from .models import Company, Spacecraft

admin.site.site_title = 'Satellite Administration'
admin.site.site_header = 'Satellite Simulation Administration'

# Register your models here.
admin.site.register(Company)
admin.site.register(Spacecraft)