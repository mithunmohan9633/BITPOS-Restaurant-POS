import os

view_code_menu = """
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
with open('core/views.py', 'a', encoding='utf-8') as f:
    f.write(view_code_menu)

url_code_menu = """
from django.urls import path
from . import views

urlpatterns = [
    path('', views.pos_dashboard, name='pos_dashboard'),
    path('users/', views.manage_users, name='manage_users'),
    path('menu/', views.manage_menu, name='manage_menu'),
]
"""
with open('core/urls.py', 'w', encoding='utf-8') as f:
    f.write(url_code_menu)

html_code_menu = """<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Manage Menu | BITPOS</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
        :root { --bg-color: #FDF8F5; --card-bg: #FFFFFF; --text-color: #4A3B32; --primary: #D38C44; --border: #E8DCCB; }
        body { margin: 0; font-family: 'Outfit', sans-serif; background: var(--bg-color); color: var(--text-color); }
        header { padding: 15px 30px; background: var(--card-bg); border-bottom: 2px solid var(--border); display: flex; justify-content: space-between; align-items: center; }
        h1 { margin: 0; font-weight: 800; font-size: 1.5rem; color: #4A3B32; }
        .container { max-width: 1000px; margin: 40px auto; padding: 20px; display: flex; gap: 30px; align-items: flex-start; }
        .column { flex: 1; display: flex; flex-direction: column; gap: 30px; }
        .card { background: var(--card-bg); border-radius: 12px; padding: 25px; border: 2px solid var(--border); box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
        .card h2 { margin-top: 0; color: var(--primary); border-bottom: 2px dashed var(--border); padding-bottom: 10px; }
        input, select, button { width: 100%; padding: 12px; margin: 10px 0; border-radius: 8px; border: 2px solid var(--border); font-family: 'Outfit', sans-serif; box-sizing: border-box; }
        button { background: var(--primary); color: white; border: none; font-weight: 800; cursor: pointer; transition: 0.2s; }
        button:hover { opacity: 0.9; }
        .menu-list { margin-top: 15px; }
        .cat-item { font-weight: 800; font-size: 1.1rem; color: var(--primary); margin-top: 15px; }
        .menu-item { display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid var(--border); }
    </style>
</head>
<body>
    <header>
        <h1>BITPOS <span style='color: var(--primary)'>?</span></h1>
        <div style='font-weight: 600; color: #8A7A6F;'>
            <a href='/users/' style='color:inherit;text-decoration:none;margin-right:20px'>Manage Users</a>
            <a href='/' style='color:inherit;text-decoration:none'>Back to POS</a>
        </div>
    </header>
    <div class='container'>
        <div class='column'>
            <div class='card'>
                <h2>Create Category</h2>
                <form method='POST'>
                    {% csrf_token %}
                    <input type='hidden' name='action' value='add_category'>
                    <select name='company' required>
                        {% for comp in companies %}
                        <option value='{{ comp.id }}'>{{ comp.name }}</option>
                        {% endfor %}
                    </select>
                    <input type='text' name='name' placeholder='Category Name (e.g. Hot Drinks)' required>
                    <button type='submit'>Add Category</button>
                </form>
            </div>

            <div class='card'>
                <h2>Create Menu Item</h2>
                <form method='POST'>
                    {% csrf_token %}
                    <input type='hidden' name='action' value='add_item'>
                    <select name='company' required>
                        {% for comp in companies %}
                        <option value='{{ comp.id }}'>{{ comp.name }}</option>
                        {% endfor %}
                    </select>
                    <select name='category' required>
                        <option value=''>-- Select Category --</option>
                        {% for cat in categories %}
                        <option value='{{ cat.id }}'>{{ cat.name }}</option>
                        {% endfor %}
                    </select>
                    <input type='text' name='name' placeholder='Item Name (e.g. Espresso)' required>
                    <input type='number' step='0.01' name='price' placeholder='Price ($)' required>
                    <button type='submit'>Add Menu Item</button>
                </form>
            </div>
        </div>

        <div class='column'>
            <div class='card'>
                <h2>Current Menu</h2>
                <div class='menu-list'>
                    {% for cat in categories %}
                        <div class='cat-item'>{{ cat.name }} ({{ cat.company.name }})</div>
                        {% for item in cat.items.all %}
                        <div class='menu-item'>
                            <span>{{ item.name }}</span>
                            <span style='font-weight:800;color:var(--primary)'>${{ item.price }}</span>
                        </div>
                        {% empty %}
                        <div class='menu-item' style='opacity:0.5'>No items yet</div>
                        {% endfor %}
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
with open('core/templates/core/manage_menu.html', 'w', encoding='utf-8') as f:
    f.write(html_code_menu)
