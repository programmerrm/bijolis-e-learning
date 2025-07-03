from django.contrib import admin
from accounts.models import User, ActiveSession

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'number']

class ActiveSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'ip_address', 'user_agent', 'last_login']

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(ActiveSession, ActiveSessionAdmin)
