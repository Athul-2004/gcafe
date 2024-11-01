from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(Customer)
admin.site.register(System)
admin.site.register(Game)
admin.site.register(Booking)
#m
# admin.py
from django.contrib.admin import AdminSite

# Override the AdminSite to change the site title and header
class CustomAdminSite(AdminSite):
    site_header = "My Custom Admin"
    site_title = "Admin Portal"
    index_title = "Welcome to My Custom Admin Portal"

# Instantiate the custom admin site
admin_site = CustomAdminSite(name='custom_admin')

# Register your models here using the custom admin site
admin_site.register(Customer)
admin_site.register(System)
admin_site.register(Game)
admin_site.register(Booking)
