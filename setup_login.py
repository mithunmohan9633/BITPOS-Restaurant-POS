import os

views_code_auth = """
from django.shortcuts import render
from django.http import HttpResponseRedirect
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
    company, _ = Company.objects.get_or_create(name='Nexus Cafe')
    
    if not Category.objects.exists():
        cat1 = Category.objects.create(company=company, name='Hot Coffees')
        cat2 = Category.objects.create(company=company, name='Cold Brews')
        cat3 = Category.objects.create(company=company, name='Pastries')
        
        MenuItem.objects.create(company=company, category=cat1, name='Espresso', price=3.50)
        MenuItem.objects.create(company=company, category=cat1, name='Latte', price=4.50)
        MenuItem.objects.create(company=company, category=cat1, name='Cappuccino', price=4.50)
        
        MenuItem.objects.create(company=company, category=cat2, name='Iced Americano', price=4.00)
        MenuItem.objects.create(company=company, category=cat2, name='Cold Brew', price=5.00)
        
        MenuItem.objects.create(company=company, category=cat3, name='Croissant', price=3.00)
        MenuItem.objects.create(company=company, category=cat3, name='Blueberry Muffin', price=3.50)

    categories = Category.objects.filter(company=company).prefetch_related('items')
    return render(request, 'core/pos_dashboard.html', {'categories': categories})

@login_required(login_url='login_view')
def manage_users(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        company_id = request.POST.get('company')

        if username and password:
            user = User.objects.create_user(username=username, email=email, password=password)
            company = Company.objects.get(id=company_id) if company_id else None
            UserProfile.objects.create(user=user, role=role, company=company)
            return HttpResponseRedirect(reverse('manage_users'))

    users = UserProfile.objects.all()
    companies = Company.objects.all()
    return render(request, 'core/manage_users.html', {'profiles': users, 'companies': companies})

@login_required(login_url='login_view')
def manage_menu(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        company_id = request.POST.get('company')
        company = Company.objects.get(id=company_id) if company_id else None

        if action == 'add_category':
            name = request.POST.get('name')
            if name and company:
                Category.objects.create(name=name, company=company)
                
        elif action == 'add_item':
            category_id = request.POST.get('category')
            name = request.POST.get('name')
            price = request.POST.get('price')
            if name and price and category_id and company:
                category = Category.objects.get(id=category_id)
                MenuItem.objects.create(name=name, price=price, category=category, company=company)
                
        return HttpResponseRedirect(reverse('manage_menu'))

    companies = Company.objects.all()
    categories = Category.objects.all().prefetch_related('items')
    return render(request, 'core/manage_menu.html', {'companies': companies, 'categories': categories})
"""
with open('core/views.py', 'w', encoding='utf-8') as f:
    f.write(views_code_auth)

url_code_auth = """
from django.urls import path
from . import views

urlpatterns = [
    path('', views.pos_dashboard, name='pos_dashboard'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('users/', views.manage_users, name='manage_users'),
    path('menu/', views.manage_menu, name='manage_menu'),
]
"""
with open('core/urls.py', 'w', encoding='utf-8') as f:
    f.write(url_code_auth)

login_html = """<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Login | BITPOS</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
        :root { --bg-color: #FDF8F5; --card-bg: #FFFFFF; --text-color: #4A3B32; --primary: #D38C44; --border: #E8DCCB; }
        body { margin: 0; font-family: 'Outfit', sans-serif; background: var(--bg-color); color: var(--text-color); height: 100vh; display: flex; align-items: center; justify-content: center; }
        .login-box { background: var(--card-bg); padding: 40px; border-radius: 16px; border: 2px solid var(--border); box-shadow: 0 10px 25px rgba(74, 59, 50, 0.08); width: 100%; max-width: 400px; text-align: center; }
        h1 { margin-top: 0; font-weight: 800; font-size: 2rem; color: #4A3B32; margin-bottom: 30px; }
        input { width: 100%; padding: 15px; margin: 10px 0; border-radius: 8px; border: 2px solid var(--border); font-family: 'Outfit', sans-serif; box-sizing: border-box; font-size: 1rem; }
        input:focus { outline: none; border-color: var(--primary); }
        button { width: 100%; padding: 15px; margin-top: 20px; background: var(--primary); color: white; border: none; border-radius: 8px; font-weight: 800; font-size: 1.1rem; cursor: pointer; transition: 0.2s; }
        button:hover { opacity: 0.9; transform: translateY(-2px); }
        .error { color: #C96459; font-weight: 600; margin-bottom: 15px; }
    </style>
</head>
<body>
    <div class='login-box'>
        <h1>BITPOS <span style='color: var(--primary)'>?</span></h1>
        {% if error %}<div class='error'>{{ error }}</div>{% endif %}
        <form method='POST'>
            {% csrf_token %}
            <input type='text' name='username' placeholder='Username' required>
            <input type='password' name='password' placeholder='Password' required>
            <button type='submit'>Sign In</button>
        </form>
    </div>
</body>
</html>"""
with open('core/templates/core/login.html', 'w', encoding='utf-8') as f:
    f.write(login_html)
