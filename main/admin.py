from django.contrib import admin
from .models import SiteSettings

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['id', 'updated_at', 'use_image']
    fieldsets = (
        (None, {
            'fields': ('background_image', 'background_color', 'use_image')
        }),
    )