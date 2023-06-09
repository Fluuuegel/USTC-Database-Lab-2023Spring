from django.contrib import admin
from .models import *

class BranchAdmin(admin.ModelAdmin):
  list_display = ("name",)
  
class StaffAdmin(admin.ModelAdmin):
  list_display = ("id", "name", "phone_number", "address", "mail", )
  
class ClientAdmin(admin.ModelAdmin):
  list_display = ("id", "name", "phone_number", "address", "mail", "contact_name", "contact_phone_number", "contact_relationship", )

admin.site.register(Branch, BranchAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Account)
admin.site.register(Loan)
admin.site.register(Client_Branch)
admin.site.register(Client_Loan)
