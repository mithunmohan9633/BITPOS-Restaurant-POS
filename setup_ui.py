html_code = """<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Nexus Cafe POS</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
        :root {
            --bg-color: #FDF8F5;
            --card-bg: #FFFFFF;
            --text-color: #4A3B32;
            --primary: #D38C44;
            --border: #E8DCCB;
        }
        body {
            margin: 0;
            font-family: 'Outfit', sans-serif;
            background: var(--bg-color);
            color: var(--text-color);
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        header {
            padding: 15px 30px;
            background: var(--card-bg);
            border-bottom: 2px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        h1 { margin: 0; font-weight: 800; font-size: 1.5rem; color: #4A3B32; }
        .main-container {
            display: flex;
            flex: 1;
            padding: 20px;
            gap: 20px;
            overflow: hidden;
        }
        .menu-section {
            flex: 2;
            display: flex;
            flex-direction: column;
            overflow-y: auto;
            padding-right: 10px;
        }
        .category-header {
            font-size: 1.2rem;
            font-weight: 800;
            margin: 10px 0;
            color: var(--primary);
        }
        .menu-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .menu-card {
            background: var(--card-bg);
            border: 2px solid var(--border);
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
        }
        .menu-card:hover {
            border-color: var(--primary);
            transform: translateY(-2px);
            box-shadow: 0 4px 10px rgba(74, 59, 50, 0.1);
        }
        .item-name { font-weight: 600; margin-bottom: 5px; }
        .item-price { color: var(--primary); font-weight: 800; }
        .order-panel {
            flex: 1;
            background: var(--card-bg);
            border-radius: 16px;
            border: 2px solid var(--border);
            padding: 20px;
            display: flex;
            flex-direction: column;
        }
    </style>
</head>
<body>
    <header>
        <h1>NEXUS CAFE <span style='color: var(--primary)'>?</span></h1>
        <div style='font-weight: 600; color: #8A7A6F;'>Direct Sale Mode</div>
    </header>
    <div class='main-container'>
        <div class='menu-section'>
            {% for category in categories %}
            <div class='category-header'>{{ category.name }}</div>
            <div class='menu-grid'>
                {% for item in category.items.all %}
                <div class='menu-card'>
                    <div class='item-name'>{{ item.name }}</div>
                    <div class='item-price'>${{ item.price }}</div>
                </div>
                {% endfor %}
            </div>
            {% endfor %}
        </div>
        <div class='order-panel'>
            <h2 style="margin-top:0; border-bottom:2px dashed var(--border); padding-bottom:15px;">New Order</h2>
            <div style="margin:auto; opacity:0.5; font-weight:500;">Tap items to add to order</div>
        </div>
    </div>
</body>
</html>"""

with open("core/templates/core/pos_dashboard.html", "w", encoding="utf-8") as f:
    f.write(html_code)

views_code = """from django.shortcuts import render
from .models import Company, Category, MenuItem

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
"""
with open("core/views.py", "w", encoding="utf-8") as f:
    f.write(views_code)
