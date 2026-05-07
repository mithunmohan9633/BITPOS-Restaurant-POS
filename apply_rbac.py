import os

views_code = """
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
            return HttpResponseRedirect(reverse('pos_dashboard'))
        else:
            return render(request, 'core/login.html', {'error': 'Invalid username or password'})
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_view'))

@login_required(login_url='login_view')
def pos_dashboard(request):
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

# Update pos_dashboard.html
path_pos = 'core/templates/core/pos_dashboard.html'
with open(path_pos, 'r', encoding='utf-8') as f:
    pos_html = f.read()

header_links = """<a href='/users/' style='color:inherit;text-decoration:none;margin-right:20px;padding:8px 12px;border:2px solid var(--border);border-radius:8px;transition:0.2s' onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">Manage Staff</a>
            <a href='/menu/' style='color:inherit;text-decoration:none;margin-right:20px;padding:8px 12px;border:2px solid var(--border);border-radius:8px;transition:0.2s' onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">Manage Menu</a>"""

protected_links = """{% if request.user.profile.role == 'admin' %}
            <a href='/users/' style='color:inherit;text-decoration:none;margin-right:20px;padding:8px 12px;border:2px solid var(--border);border-radius:8px;transition:0.2s' onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">Manage Staff</a>
            <a href='/menu/' style='color:inherit;text-decoration:none;margin-right:20px;padding:8px 12px;border:2px solid var(--border);border-radius:8px;transition:0.2s' onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">Manage Menu</a>
            {% endif %}"""

if header_links in pos_html:
    pos_html = pos_html.replace(header_links, protected_links)
with open(path_pos, 'w', encoding='utf-8') as f:
    f.write(pos_html)


# Update manage_users.html to remove company select
path_users = 'core/templates/core/manage_users.html'
with open(path_users, 'r', encoding='utf-8') as f:
    users_html = f.read()

# remove company dropdown
import re
users_html = re.sub(r"<select name='company'>.*?</select>", "", users_html, flags=re.DOTALL)
with open(path_users, 'w', encoding='utf-8') as f:
    f.write(users_html)


# Update manage_menu.html to remove company select
path_menu = 'core/templates/core/manage_menu.html'
with open(path_menu, 'r', encoding='utf-8') as f:
    menu_html = f.read()

menu_html = re.sub(r"<select name='company' required>.*?</select>", "", menu_html, flags=re.DOTALL)
with open(path_menu, 'w', encoding='utf-8') as f:
    f.write(menu_html)

