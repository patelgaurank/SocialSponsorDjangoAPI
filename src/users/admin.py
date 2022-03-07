from django.contrib import admin
from .models import NewUser, AuditEntry, NewUserInfo, ZoneInfo, ZoneSOLeaderInfo, SatsangCategoryInfo, MandalInfo, NewUserAddress
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('email', 'user_name', 'phone_number',)
    list_filter = ('email', 'user_name', 'phone_number', 'is_active', 'is_staff')
    ordering = ('email',)
    list_display = ('email', 'id', 'user_name', 'phone_number', 'is_admin',
                    'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'phone_number',)}),
        ('Permissions', {'fields': ('is_admin', 'is_staff',
                                    'is_active', 'groups', 'user_permissions')}),
        ('Personal', {'fields': ('about',)}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'phone_number', 'password1', 'password2')}
         ),
    )


admin.site.register(NewUser, UserAdminConfig)


@admin.register(AuditEntry)
class AuditEntryAdmin(admin.ModelAdmin):
    list_display = ['action', 'email', 'ip', ]
    list_filter = ['created_at', 'action', ]

@admin.register(NewUserInfo)
class NewUserInfoAdmin(admin.ModelAdmin):
    list_display = ['IMS_Member_Id', 'first_name', 'last_name', ]
    list_filter = ['created_at', 'first_name']

@admin.register(ZoneInfo)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ['Zone_Id', 'Zone', 'Direction', ]
    list_filter = ['created_at', 'Zone']

@admin.register(MandalInfo)
class MandalAdmin(admin.ModelAdmin):
    list_display = ['Mandal_Id', 'Mandal',]
    list_filter = ['created_at','Mandal']

@admin.register(SatsangCategoryInfo)
class SatsangCategoryAdmin(admin.ModelAdmin):
    list_display = ['SatsangCategory_Id', 'SatsangCategory',]
    list_filter = ['created_at','SatsangCategory']

@admin.register(ZoneSOLeaderInfo)
class ZoneSOLeaderAdmin(admin.ModelAdmin):
    list_display = ['ZoneSOLeader_Id', 'Zone_SO_Leader', 'Zone_SO_Karyakar',]
    list_filter = ['created_at','Zone_SO_Leader', 'Zone_SO_Karyakar']
# 

@admin.register(NewUserAddress)
class NewUserAddressAdmin(admin.ModelAdmin):
    list_display = ['NewUserAddress_Id', 'email',]
    list_filter = ['created_at','email', 'Address1']