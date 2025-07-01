from django.contrib import admin
from accounts.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'number']

# Register your models here.
admin.site.register(User, UserAdmin)
