from django.contrib import admin
from .models import Branch, Staff, Client

class BranchAdmin(admin.ModelAdmin):
  list_display = ("name",)
  
class StaffAdmin(admin.ModelAdmin):
  list_display = ("id", "name", "phone_number", "address", "mail", )

class ClientAdmin(admin.ModelAdmin):
  list_display = ("id", "name", "phone_number", "address", "mail", "contact_name", "contact_phone_number", "contact_relationship", )

admin.site.register(Branch, BranchAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Client, ClientAdmin)
