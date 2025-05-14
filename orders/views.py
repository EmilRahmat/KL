from django.shortcuts import get_object_or_404, redirect
from cart.models import CartItem, Cart
from goods.models import Variation
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import notify_telegram

@login_required
def create_order(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect('cart:cart_detail')

    # создаём заказ без total_price (временно)
    order = Order.objects.create(
        user=request.user,
        status='pending'  # status исправлен на корректный
    )

    total_price = 0

    for item in cart_items:
        item_price = item.product.price
        OrderItem.objects.create(
            order=order,
            product=item.product,
            variation=item.variation,
            quantity=item.quantity,
            price=item_price
        )
        total_price += item_price * item.quantity

        item.variation.quantity -= item.quantity
        item.variation.save()

    # обновляем total_price после создания
    order.total_price = total_price
    order.save()

    cart_items.delete()

    notify_telegram(order)
    
    return redirect('users:profile')

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)

    if order.status in ['pending', 'waiting_payment', 'processing']:
        for item in order.items.all():
            item.variation.quantity += item.quantity
            item.variation.save()
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'Заказ успешно отменён.')
    else:
        messages.warning(request, 'Невозможно отменить заказ на текущей стадии.')

    return redirect('users:profile')