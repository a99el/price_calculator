# في ملف pricing/urls.py
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from pricing import views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('offer_detail/', views.offer_detail, name='offer_detail'),
]
