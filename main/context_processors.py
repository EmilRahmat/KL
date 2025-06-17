from .models import SiteSettings
from django.db.models import Sum
from cart.models import Cart, CartItem

def site_settings(request):
    settings = SiteSettings.objects.last()  # Последняя запись
    return {
        'site_settings': settings
    }

def cart_item_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0
        else:
            count = 0
    else:
        count = 0
    return {'cart_item_count': count}