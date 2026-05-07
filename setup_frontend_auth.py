import os

view_code = """
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import UserProfile

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
"""
with open('core/views.py', 'a', encoding='utf-8') as f:
    f.write(view_code)

url_code = """
from django.urls import path
from . import views

urlpatterns = [
    path('', views.pos_dashboard, name='pos_dashboard'),
    path('users/', views.manage_users, name='manage_users'),
]
"""
with open('core/urls.py', 'w', encoding='utf-8') as f:
    f.write(url_code)

html_code = """<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Manage Users | BITPOS</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
        :root {
            --bg-color: #FDF8F5;
            --card-bg: #FFFFFF;
            --text-color: #4A3B32;
            --primary: #D38C44;
            --border: #E8DCCB;
        }
        body { margin: 0; font-family: 'Outfit', sans-serif; background: var(--bg-color); color: var(--text-color); }
        header { padding: 15px 30px; background: var(--card-bg); border-bottom: 2px solid var(--border); display: flex; justify-content: space-between; align-items: center; }
        h1 { margin: 0; font-weight: 800; font-size: 1.5rem; color: #4A3B32; }
        .container { max-width: 800px; margin: 40px auto; padding: 20px; }
        .card { background: var(--card-bg); border-radius: 12px; padding: 25px; border: 2px solid var(--border); box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 30px; }
        .card h2 { margin-top: 0; color: var(--primary); }
        input, select, button { width: 100%; padding: 12px; margin: 10px 0; border-radius: 8px; border: 2px solid var(--border); font-family: 'Outfit', sans-serif; box-sizing: border-box; }
        button { background: var(--primary); color: white; border: none; font-weight: 800; cursor: pointer; transition: 0.2s; }
        button:hover { opacity: 0.9; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { text-align: left; padding: 12px; border-bottom: 1px solid var(--border); }
    </style>
</head>
<body>
    <header>
        <h1>BITPOS <span style='color: var(--primary)'>?</span></h1>
        <div style='font-weight: 600; color: #8A7A6F;'><a href='/' style='color:inherit;text-decoration:none'>Back to POS</a></div>
    </header>
    <div class='container'>
        <div class='card'>
            <h2>Create New Staff User</h2>
            <form method='POST'>
                {% csrf_token %}
                <input type='text' name='username' placeholder='Username' required>
                <input type='email' name='email' placeholder='Email (Optional)'>
                <input type='password' name='password' placeholder='Password' required>
                <select name='role'>
                    <option value='cashier_restaurant'>Restaurant Cashier</option>
                    <option value='cashier_retail'>Retail Cashier</option>
                    <option value='admin'>Store Admin</option>
                </select>
                <select name='company'>
                    {% for comp in companies %}
                    <option value='{{ comp.id }}'>{{ comp.name }}</option>
                    {% endfor %}
                </select>
                <button type='submit'>Create User</button>
            </form>
        </div>

        <div class='card'>
            <h2>Existing Staff</h2>
            <table>
                <tr><th>Username</th><th>Role</th><th>Company</th></tr>
                {% for profile in profiles %}
                <tr>
                    <td>{{ profile.user.username }}</td>
                    <td>{{ profile.get_role_display }}</td>
                    <td>{{ profile.company.name|default:"None" }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </div>
</body>
</html>"""
with open('core/templates/core/manage_users.html', 'w', encoding='utf-8') as f:
    f.write(html_code)
