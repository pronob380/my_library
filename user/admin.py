from django.contrib import admin

from accounts import models
from .models import User
class UserAdmin(admin.ModelAdmin):
    # List of fields to display in the list view
    list_display = ('email', 'name', 'roll', 'department', 'session', 'phone_number', 'is_active', 'is_admin', 'user_type')
    
    # Fields to be included in the detail view form
    fields = (
        'email', 'name', 'roll', 'department', 'session', 'phone_number', 'address', 'membership_number', 'user_type', 'image', 'is_active', 'is_admin'
    )
    
   
    # Fields to be included in the search functionality
    search_fields = ('email', 'name', 'roll', 'department', 'session', 'phone_number', 'membership_number')
    
    # Fields to be read-only in the detail view
    readonly_fields = ('email', 'membership_number')

   

admin.site.register(User, UserAdmin)