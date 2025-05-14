from .models import SiteSettings

def site_settings(request):
    settings = SiteSettings.objects.last()  # Последняя запись
    return {
        'site_settings': settings
    }
