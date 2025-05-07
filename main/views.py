from django.http import HttpResponse
from django.shortcuts import render
from goods.models import Categories

def index(request):
    
    
    
    context: dict = {
        'title': 'KidsLook - Главная',
        "content": 'Магазин KidsLook',
    }
    
    return render(request, 'main/index.html', context)

def about(request):
    about: dict = {
        'title': 'KidsLook - О нас',
        "content": 'О нас',
        'text_on_page': 'KidsLook - стильная и качественная одежда для юных модниц. - Более 1000 довольных Клиентов - Постоянные розыгрыши и интересный контент'
        
    }
    
    return render(request, 'main/about.html', about)