import random
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import PhoneLoginForm, CodeVerificationForm, PhoneNumberForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import make_password
from orders.models import Order

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
        form = PhoneNumberForm(request.POST)
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
                if created:
                    user.set_unusable_password()
                    user.save()

                if user.has_usable_password():
                    login(request, user)
                    return redirect('users:profile')
                else:
                    # не логиним сразу, только сохраняем user_id в сессии
                    request.session['temp_user_id'] = user.id
                    return redirect('users:set_password')
            else:
                messages.error(request, "Неверный код.")
    else:
        form = CodeVerificationForm()
    return render(request, 'users/verify_code.html', {'form': form})



@csrf_protect
def logout_view(request):
    logout(request)
    return redirect('main:index')


def set_password_view(request):
    user = None
    if request.user.is_authenticated:
        user = request.user
        print("Пользователь уже аутентифицирован:", user)
    else:
        user_id = request.session.get('temp_user_id')
        print("temp_user_id из сессии:", user_id)
        if user_id:
            try:
                user = CustomUser.objects.get(id=user_id)
                print("Пользователь найден по ID:", user)
            except CustomUser.DoesNotExist:
                print("Пользователь не найден")

    if not user:
        print("Пользователь не определён, редиректим на вход")
        return redirect('users:phone_login')

    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print("Получены пароли:", password1, password2)

        if password1 != password2:
            messages.error(request, "Пароли не совпадают.")
        elif len(password1) < 6:
            messages.error(request, "Пароль должен быть не менее 6 символов.")
        else:
            user.set_password(password1)
            user.save()
            login(request, user)
            messages.success(request, "Пароль успешно установлен.")
            return redirect('users:profile')

    return render(request, 'users/set_password.html')


@login_required
def profile_view(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'users/profile.html', {'orders': user_orders})