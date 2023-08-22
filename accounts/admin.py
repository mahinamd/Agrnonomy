from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Token, Notification


# Account admin
class AccountAdmin(UserAdmin):
    list_display = ('id', 'date_joined', 'last_login', 'is_superuser', 'is_admin', 'is_staff', 'is_expert', 'is_verified', 'is_active', 'image', 'first_name', 'last_name', 'email', 'phone', 'password', 'reputation')
    search_fields = ('id', 'date_joined', 'last_login', 'first_name', 'last_name', 'email', 'phone')
    readonly_fields = ('id', 'date_joined', 'last_login')
    ordering = ('id', 'date_joined', 'last_login')


admin.site.register(Account, AccountAdmin)


# Token admin
class TokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'last_modified', 'account', 'token', 'expire_date', 'is_valid')
    search_fields = ('id', 'created', 'last_modified', 'account', 'token', 'expire_date')
    readonly_fields = ('id', 'created', 'last_modified')
    ordering = ('id', 'created', 'last_modified')


admin.site.register(Token, TokenAdmin)


# Notification admin
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'account', 'created_by', 'notification', "read")
    search_fields = ('id', 'timestamp', 'account', "created_by", "notification")
    readonly_fields = ('id', 'timestamp')
    ordering = ('id', 'timestamp')


admin.site.register(Notification, NotificationAdmin)
