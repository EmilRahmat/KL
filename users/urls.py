from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.phone_login_view, name='phone_login'),
    path('verify/', views.verify_code_view, name='verify_code'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]