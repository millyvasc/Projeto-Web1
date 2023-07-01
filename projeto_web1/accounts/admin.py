from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .forms import CustomerUserForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomerUserForm
    form = CustomerUserForm

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)