urls_code = """
from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path('', views.pos_dashboard, name='pos_dashboard'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('users/', views.manage_users, name='manage_users'),
    path('menu/', views.manage_menu, name='manage_menu'),
    path('super-admin/', views.super_admin_dashboard, name='super_admin_dashboard'),
    path('super-admin/create-company/', views.super_admin_create_company, name='super_admin_create_company'),
    path('super-admin/create-admin/', views.super_admin_create_admin, name='super_admin_create_admin'),
    path('super-admin/toggle-company/<int:company_id>/', views.super_admin_toggle_company, name='super_admin_toggle_company'),
    path('api/companies/', api_views.get_companies, name='api_companies'),
    path('api/users/', api_views.manage_users_api, name='api_users'),
    path('api/menu/', api_views.get_menu, name='api_menu'),
]
"""
with open('core/urls.py', 'w', encoding='utf-8') as f:
    f.write(urls_code)
