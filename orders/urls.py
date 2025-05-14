from django.urls import path
from .views import create_order, cancel_order

app_name = 'orders'

urlpatterns = [
    path('create/', create_order, name='create_order'),
    path('cancel/<int:order_id>/', cancel_order, name='cancel_order'),
]