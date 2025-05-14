from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from .forms import PhoneLoginForm

app_name = 'users'

urlpatterns = [
    path('login/', views.phone_login_view, name='phone_login'),
    path('login/password/', LoginView.as_view(
    template_name='users/login_password.html',
    authentication_form=PhoneLoginForm,
    redirect_authenticated_user=True
), name='login_password'),
    path('verify/', views.verify_code_view, name='verify_code'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('set-password/', views.set_password_view, name='set_password'),
    
]