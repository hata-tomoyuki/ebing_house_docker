# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.utils.translation import gettext_lazy as _ 

# from .models import CustomUser

# # Register your models here.

# class CustomUserAdmin(UserAdmin):
#     fieldsets = (
#         (None, {'fields':('username','password')}),
#         (_('Personal info'), {'fields':('first_name','last_name','email','age')}),
#         (_('Permissions'), {'fields':('is_active','is_staff','is_superuser',
#                                       'groups','user_permission')}),
#         (_('Important dates'), {'fields':('last_login','date_joined')}),         
#     )

# admin.site.register(CustomUser, CustomUserAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('age',)}),  # カスタムフィールド 'age' を追加
    )

admin.site.register(CustomUser, CustomUserAdmin)