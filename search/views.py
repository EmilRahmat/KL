from django.shortcuts import render
from goods.models import Products
from django.db.models import Q
from rapidfuzz import fuzz

def search_view(request):
    COLOR_DICT = {
        'black': 'черный',
        'white': 'белый',
        'red': 'красный',
        'beige': 'бежевый',
        'khaki': 'хаки',
        'ping': 'розовый',
        'vio;': 'фиолетовый',
        'blue': 'синий',
        'green': 'зеленый',
        'yellow': 'желтый',
        'grey': 'серый',
        'brown': 'коричневый',
        'burgundy': 'бордовый',
    }

    query = request.GET.get('q', '').strip()
    results = []

    if query:
        words = query.lower().split()

        all_products = Products.objects.prefetch_related('variations').all()

        for product in all_products:
            product_name = product.name.lower()

            sizes = [variation.size.lower() for variation in product.variations.all() if variation.size]

            colors = []
            for variation in product.variations.all():
                if variation.color:
                    colors.append(COLOR_DICT.get(variation.color, variation.color).lower())

            # Проверяем, что для каждого слова оно есть в названии или размерах или цветах
            if all(
                any(word in field for field in [product_name] + sizes + colors)
                for word in words
            ):
                results.append(product)

    return render(request, 'search/results.html', {
        'query': query,
        'results': results,
    })