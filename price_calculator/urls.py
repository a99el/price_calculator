# في ملف price_calculator/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from pricing import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('offer_detail/', views.offer_detail_view, name='offer_detail'),
    path('add_user/', views.add_user_view, name='add_user'),
]
