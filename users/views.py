import random
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import PhoneLoginForm, CodeVerificationForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

def send_sms_code(phone, code):
    response = requests.post("https://textbelt.com/text", {
        "phone": phone,
        "message": f"Your login code is: {code}",
        "key": "textbelt"  # используем бесплатный API-ключ для тестов
    })
    return response.json()

def phone_login_view(request):
    if request.method == 'POST':
        print("POST данные:", request.POST)  # временно для отладки
        form = PhoneLoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            code = random.randint(1000, 9999)
            print("Сгенерированный код:", code)  # тоже для отладки
            request.session['code'] = str(code)
            request.session['phone_number'] = phone_number
            send_sms_code(phone_number, code)
            return redirect('users:verify_code')  # обязательно 'users:verify_code'
        else:
            print("Форма невалидна:", form.errors)
    else:
        form = PhoneLoginForm()
    return render(request, 'users/phone_login.html', {'form': form})

def verify_code_view(request):
    if request.method == 'POST':
        form = CodeVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if code == request.session.get('code'):
                phone = request.session.get('phone_number')
                user, created = CustomUser.objects.get_or_create(phone_number=phone)
                login(request, user)
                return redirect('users:profile')
            else:
                messages.error(request, "Invalid code.")
    else:
        form = CodeVerificationForm()
    return render(request, 'users/verify_code.html', {'form': form})

@csrf_protect
def logout_view(request):
    logout(request)
    return redirect('main:index')

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')