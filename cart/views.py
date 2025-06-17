from django.db import models
from django.conf import settings
from goods.models import Products, Variation
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path
from django.contrib.auth.decorators import login_required
from .utils import get_or_create_cart
from .models import Cart, CartItem
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
@require_POST
def add_to_cart_view(request, product_id):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Только AJAX-запросы'}, status=400)

    product = get_object_or_404(Products, id=product_id)
    variation_id = request.POST.get('variation_id')
    if not variation_id:
        return JsonResponse({'success': False, 'error': 'variation_id не передан'}, status=400)

    variation = get_object_or_404(Variation, id=variation_id)

    cart = get_or_create_cart(request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product, variation=variation)
    if not created:
        item.quantity += 1
    item.save()

    cart_item_count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0

    return JsonResponse({'success': True, 'cart_item_count': cart_item_count})


@login_required
def cart_detail_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

@login_required
def remove_from_cart_view(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart:cart_detail')


@login_required
def update_quantity_view(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity'))
        item.quantity = max(1, new_quantity)
        item.save()
    return redirect('cart:cart_detail')

def cart_view(request):
    return render(request, "cart/detail.html")