views_code = r"""
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Company, Category, MenuItem, UserProfile


def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return HttpResponseRedirect(reverse('super_admin_dashboard'))
            elif hasattr(user, 'profile') and user.profile.role == 'admin':
                return HttpResponseRedirect(reverse('pos_dashboard'))
            else:
                return HttpResponseRedirect(reverse('pos_dashboard'))
        else:
            return render(request, 'core/login.html', {'error': 'Invalid username or password'})
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_view'))


@login_required(login_url='login_view')
def super_admin_dashboard(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Access Denied: Super Admin only.")
    companies = Company.objects.all().order_by('-created_at')
    admins = UserProfile.objects.filter(role='admin').select_related('user', 'company')
    return render(request, 'core/super_admin.html', {
        'companies': companies,
        'admins': admins,
    })


@login_required(login_url='login_view')
def super_admin_create_company(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Access Denied.")
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address', '')
        pos_type = request.POST.get('pos_type', 'restaurant')
        if name:
            Company.objects.create(name=name, address=address, pos_type=pos_type)
    return HttpResponseRedirect(reverse('super_admin_dashboard'))


@login_required(login_url='login_view')
def super_admin_create_admin(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Access Denied.")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        company_id = request.POST.get('company')
        if username and password and company_id:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)
                company = Company.objects.get(id=company_id)
                UserProfile.objects.create(user=user, role='admin', company=company)
    return HttpResponseRedirect(reverse('super_admin_dashboard'))


@login_required(login_url='login_view')
def super_admin_toggle_company(request, company_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Access Denied.")
    company = Company.objects.get(id=company_id)
    company.is_active = not company.is_active
    company.save()
    return HttpResponseRedirect(reverse('super_admin_dashboard'))


@login_required(login_url='login_view')
def pos_dashboard(request):
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('super_admin_dashboard'))
    if not hasattr(request.user, 'profile') or not request.user.profile.company:
        return HttpResponseForbidden("Your account is not assigned to any store.")
    company = request.user.profile.company
    categories = Category.objects.filter(company=company).prefetch_related('items')
    return render(request, 'core/pos_dashboard.html', {'categories': categories})


@login_required(login_url='login_view')
def manage_users(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        return HttpResponseForbidden("Access Denied: Only Store Admins can manage users.")
    company = request.user.profile.company
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        if username and password:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)
                UserProfile.objects.create(user=user, role=role, company=company)
            return HttpResponseRedirect(reverse('manage_users'))
    profiles = UserProfile.objects.filter(company=company)
    return render(request, 'core/manage_users.html', {'profiles': profiles})


@login_required(login_url='login_view')
def manage_menu(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        return HttpResponseForbidden("Access Denied: Only Store Admins can manage the menu.")
    company = request.user.profile.company
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_category':
            name = request.POST.get('name')
            if name:
                Category.objects.create(name=name, company=company)
        elif action == 'add_item':
            category_id = request.POST.get('category')
            name = request.POST.get('name')
            price = request.POST.get('price')
            if name and price and category_id:
                category = Category.objects.get(id=category_id, company=company)
                MenuItem.objects.create(name=name, price=price, category=category, company=company)
        return HttpResponseRedirect(reverse('manage_menu'))
    categories = Category.objects.filter(company=company).prefetch_related('items')
    return render(request, 'core/manage_menu.html', {'categories': categories})
"""

with open('core/views.py', 'w', encoding='utf-8') as f:
    f.write(views_code)
