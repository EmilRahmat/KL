
from django.urls import path

from . import views

app_name = 'goods'

urlpatterns = [
    path('<slug:category_slug>/', views.CatalogView.as_view(), name='index'),
    path('product/<slug:product_slug>/', views.ProductView.as_view(), name='product'),
    path('notify-restock/<int:product_id>/', views.notify_restock, name='notify_restock'),
] 