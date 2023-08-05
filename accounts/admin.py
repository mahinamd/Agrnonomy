from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Notification


# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('id', 'date_joined', 'last_login', 'is_admin', 'is_active', 'is_staff', 'expert', 'is_superuser', 'is_verified', 'phone', 'pimg', 'fname', 'lname', 'email', 'password')
    search_fields = ('phone', 'fname', 'lname', 'email')
    readonly_fields = ('id', 'date_joined', 'last_login')
    ordering = ('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)


# Notification admin
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'account', 'created_by', 'notification', "read")
    search_fields = ('id', 'timestamp', 'account', "created_by", "notification")
    readonly_fields = ('id', 'timestamp')
    ordering = ('id', 'timestamp')


admin.site.register(Notification, NotificationAdmin)
