# from django.db.models import Sum
# from .models import Cart

# def cart_items_count(request):
#     count = 0
#     if request.user.is_authenticated:
#         try:
#             cart = Cart.objects.get(user=request.user)
#             count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0
#         except Cart.DoesNotExist:
#             count = 0
#     return {'cart_items_count': count}
