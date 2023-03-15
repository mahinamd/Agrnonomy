from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('id', 'date_joined', 'last_login', 'is_admin', 'is_active', 'is_staff', 'is_superuser', 'is_verified', 'phone', 'pimg', 'fname', 'lname', 'gender', 'dob', 'email', 'password', 'house_no', 'address_line', 'city', 'zip_code', 'country', 'social_li', 'social_fb', 'social_tw')
    search_fields = ('phone', 'fname', 'lname', 'email', 'house_no', 'address_line', 'city', 'zip_code', 'country',)
    readonly_fields = ('id', 'date_joined', 'last_login')
    ordering = ('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
