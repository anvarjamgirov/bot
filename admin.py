from django.contrib import admin

from bot import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_time'
    list_display = [
        'id',
        'user_id',
        'full_name',
        'username',
        'is_active',
        'is_admin'
    ]
    list_filter = [
        'is_active',
        'is_admin'
    ]
    search_fields = [
        'full_name',
        'user_id',
        'username',
    ]
    exclude = [
        'step',
        'data',
        'created_time'
    ]


@admin.register(models.Constant)
class ConstantAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_time'
    list_display = [
        'key',
        'data',
        'created_time'
    ]
    search_fields = [
        'key',
    ]
    exclude = [
        'created_time'
    ]


@admin.register(models.Text)
class TextAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_time'
    list_display = [
        'id',
        'language',
        'created_time'
    ]
    search_fields = [
        'language',
    ]
    exclude = [
        'created_time'
    ]


@admin.register(models.Log)
class LogAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_time'
    list_display = [
        'id',
        'user',
        'reason',
        'created_time'
    ]
    search_fields = [
        'user__full_name',
        'text',
    ]
    list_filter = [
        'reason'
    ]
    exclude = [
        'created_time'
    ]
