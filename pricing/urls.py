from django.urls import path
from pricing import views
from django.contrib.auth import views as auth_views

app_name = 'pricing'  # تحديد اسم التطبيق لضمان التميز في النطاقات

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('offer_detail/', views.offer_detail_view, name='offer_detail'),
    path('update_statement/', views.update_statement, name='update_statement'),  # إضافة هذا السطر
    path('delete_user/<int:user_id>/', views.delete_user_view, name='delete_user'),  # إضافة هذا السطر
]