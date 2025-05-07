from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView
from django.db.models import Q, Min, Max
from goods.models import Gallery, Products, Categories, Variation

class CatalogView(ListView):
    model = Products
    template_name = 'goods/catalog.html'
    context_object_name = 'goods'
    paginate_by = 9  # можно увеличить, если нужно

    def get_queryset(self):
        queryset = Products.objects.filter(is_available=True).distinct()
        category_slug = self.kwargs.get('category_slug')

        if category_slug and category_slug not in ['vse-tovary', 'sale']:
            queryset = queryset.filter(Q(category__slug=category_slug) | Q(category__parent__slug=category_slug))
        elif category_slug == 'sale':
            queryset = queryset.filter(discount__gt=0)

        # Фильтрация по размеру (мультивыбор)
        selected_sizes = self.request.GET.getlist('size')
        if selected_sizes:
            queryset = queryset.filter(variations__size__in=selected_sizes)

        # Фильтрация по диапазону цен
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Фильтрация по акции
        if self.request.GET.get('on_sale'):
            queryset = queryset.filter(discount__gt=0)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        
        context['title'] = 'KidsLook - Каталог'
        context['category_slug'] = category_slug
        context['images'] = Gallery.objects.all()
        context['all_categories'] = Categories.objects.all().prefetch_related('subcategory')

        # Получаем все доступные размеры
        sizes = Variation.objects.values_list('size', flat=True).distinct().order_by('size')
        context['sizes'] = [size for size in sizes if size]  # убираем None

        # Выбранные размеры для чекбоксов
        context['selected_sizes'] = self.request.GET.getlist('size')

        return context   


class ProductView(DetailView):
    model = Products
    template_name = 'goods/product.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        context["ext_product"] = Products.objects.exclude(slug=self.kwargs['product_slug']).order_by('?')[:4]
        
        context['available_variations'] = product.variations.filter(quantity__gt=0)
        context['unavailable_variations'] = product.variations.filter(quantity=0)
        return context

@csrf_exempt  # Только если ты тестируешь, лучше использовать CSRF-токен!
def notify_restock(request, product_id):
    if request.method == 'POST':
        email = request.POST.get('email')
        size = request.POST.get('size')
        # Здесь можно сохранить уведомление в БД или отправить email

        # Временно просто логируем:
        print(f"Запрос на уведомление: продукт {product_id}, размер {size}, email {email}")

        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'method not allowed'}, status=405)