# Fix 1: Unified dark theme for all admin pages

# Order History - Dark Theme
order_history_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Order History | BITPOS</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root { --bg: #1A1A2E; --card: #16213E; --primary: #D38C44; --accent: #0F3460; --text: #E8E8E8; --muted: #8892B0; --success: #4ECB71; --purple: #6366F1; --danger: #E94560; --border: #233554; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Outfit', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }
        header { background: var(--card); padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--border); }
        h1 { font-weight: 800; font-size: 1.5rem; color: var(--primary); }
        .nav-links a { color: var(--muted); text-decoration: none; margin-left: 20px; font-weight: 600; padding: 6px 12px; border-radius: 6px; transition: 0.2s; }
        .nav-links a:hover { color: var(--primary); background: rgba(211,140,68,0.1); }
        .container { max-width: 1100px; margin: 30px auto; padding: 0 20px; }
        h2 { margin-bottom: 20px; color: var(--primary); }
        .search-bar { display: flex; gap: 10px; margin-bottom: 25px; }
        .search-bar input { flex: 1; padding: 14px; border-radius: 8px; border: 2px solid var(--border); background: var(--card); color: var(--text); font-family: 'Outfit', sans-serif; font-size: 1rem; }
        .search-bar input:focus { outline: none; border-color: var(--primary); }
        .search-bar input::placeholder { color: var(--muted); }
        .search-bar button { padding: 14px 25px; background: var(--primary); color: white; border: none; border-radius: 8px; font-weight: 800; cursor: pointer; }
        table { width: 100%; border-collapse: collapse; background: var(--card); border-radius: 12px; overflow: hidden; }
        th { background: var(--accent); color: var(--text); text-align: left; padding: 15px 20px; font-weight: 800; font-size: 0.8rem; letter-spacing: 1px; text-transform: uppercase; }
        td { padding: 15px 20px; border-bottom: 1px solid var(--border); }
        tr:last-child td { border-bottom: none; }
        tr:hover td { background: rgba(211,140,68,0.05); }
        .order-link { color: var(--primary); font-weight: 800; text-decoration: none; }
        .order-link:hover { text-decoration: underline; }
        .badge { padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 800; }
        .badge-cash { background: rgba(78,203,113,0.15); color: var(--success); }
        .badge-upi { background: rgba(99,102,241,0.15); color: var(--purple); }
        .badge-split { background: rgba(211,140,68,0.15); color: var(--primary); }
    </style>
</head>
<body>
    <header>
        <h1>BITPOS</h1>
        <div class="nav-links">
            <a href="/sales/">Sales</a>
            <a href="/orders/">Orders</a>
            <a href="/menu/">Menu</a>
            <a href="/users/">Staff</a>
            <a href="/logout/" style="color:#E94560">Logout</a>
        </div>
    </header>
    <div class="container">
        <h2>Order History</h2>
        <form class="search-bar" method="GET">
            <input type="text" name="search" placeholder="Search by Order Number..." value="{{ search }}">
            <button type="submit">Search</button>
        </form>
        <table>
            <tr><th>Order #</th><th>Date & Time</th><th>Amount</th><th>Payment</th><th>Billed By</th><th>Actions</th></tr>
            {% for order in orders %}
            <tr>
                <td><a href="/orders/{{ order.order_number }}/" class="order-link">{{ order.order_number }}</a></td>
                <td style="color:var(--muted)">{{ order.created_at|date:"d M Y, h:i A" }}</td>
                <td style="font-weight:800; color:var(--primary)">&#8377;{{ order.total_amount }}</td>
                <td><span class="badge {% if order.payment_method == 'cash' %}badge-cash{% elif order.payment_method == 'upi' %}badge-upi{% else %}badge-split{% endif %}">{{ order.get_payment_method_display }}</span></td>
                <td>{{ order.billed_by.username|default:"--" }}</td>
                <td><a href="/bill/{{ order.order_number }}/" class="order-link" target="_blank">View Bill</a></td>
            </tr>
            {% empty %}
            <tr><td colspan="6" style="text-align:center; padding:40px; color:var(--muted)">No orders found</td></tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>"""
with open('core/templates/core/order_history.html', 'w', encoding='utf-8') as f:
    f.write(order_history_html)


# Manage Users - Dark Theme
manage_users_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Manage Staff | BITPOS</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root { --bg: #1A1A2E; --card: #16213E; --primary: #D38C44; --accent: #0F3460; --text: #E8E8E8; --muted: #8892B0; --border: #233554; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Outfit', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }
        header { background: var(--card); padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--border); }
        h1 { font-weight: 800; font-size: 1.5rem; color: var(--primary); }
        .nav-links a { color: var(--muted); text-decoration: none; margin-left: 20px; font-weight: 600; padding: 6px 12px; border-radius: 6px; transition: 0.2s; }
        .nav-links a:hover { color: var(--primary); background: rgba(211,140,68,0.1); }
        .container { max-width: 900px; margin: 30px auto; padding: 0 20px; display: flex; gap: 30px; align-items: flex-start; }
        .card { background: var(--card); border-radius: 16px; padding: 30px; border: 1px solid var(--border); flex: 1; }
        .card h2 { color: var(--primary); margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px dashed var(--border); }
        input, select { width: 100%; padding: 14px; margin: 8px 0; border-radius: 8px; border: 2px solid var(--border); background: var(--bg); color: var(--text); font-family: 'Outfit', sans-serif; font-size: 1rem; }
        input:focus, select:focus { outline: none; border-color: var(--primary); }
        input::placeholder { color: var(--muted); }
        button { width: 100%; padding: 14px; margin-top: 15px; background: var(--primary); color: white; border: none; border-radius: 8px; font-weight: 800; font-size: 1rem; cursor: pointer; transition: 0.2s; }
        button:hover { opacity: 0.9; }
        .user-row { display: flex; justify-content: space-between; padding: 15px; border-bottom: 1px solid var(--border); align-items: center; }
        .user-row:last-child { border-bottom: none; }
    </style>
</head>
<body>
    <header>
        <h1>BITPOS</h1>
        <div class="nav-links">
            <a href="/sales/">Sales</a>
            <a href="/orders/">Orders</a>
            <a href="/menu/">Menu</a>
            <a href="/users/">Staff</a>
            <a href="/logout/" style="color:#E94560">Logout</a>
        </div>
    </header>
    <div class="container">
        <div class="card">
            <h2>Create New Staff</h2>
            <form method="POST">
                {% csrf_token %}
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <select name="role">
                    <option value="cashier_restaurant">Restaurant Cashier</option>
                    <option value="cashier_retail">Retail Cashier</option>
                </select>
                <button type="submit">Create User</button>
            </form>
        </div>
        <div class="card">
            <h2>Existing Staff</h2>
            {% for profile in profiles %}
            <div class="user-row">
                <span style="font-weight:800">{{ profile.user.username }}</span>
                <span style="color:var(--primary); font-weight:600">{{ profile.get_role_display }}</span>
            </div>
            {% empty %}
            <div style="text-align:center; padding:30px; color:var(--muted)">No staff members yet</div>
            {% endfor %}
        </div>
    </div>
</body>
</html>"""
with open('core/templates/core/manage_users.html', 'w', encoding='utf-8') as f:
    f.write(manage_users_html)


# Manage Menu - Dark Theme
manage_menu_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Manage Menu | BITPOS</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root { --bg: #1A1A2E; --card: #16213E; --primary: #D38C44; --accent: #0F3460; --text: #E8E8E8; --muted: #8892B0; --border: #233554; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Outfit', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }
        header { background: var(--card); padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--border); }
        h1 { font-weight: 800; font-size: 1.5rem; color: var(--primary); }
        .nav-links a { color: var(--muted); text-decoration: none; margin-left: 20px; font-weight: 600; padding: 6px 12px; border-radius: 6px; transition: 0.2s; }
        .nav-links a:hover { color: var(--primary); background: rgba(211,140,68,0.1); }
        .container { max-width: 1100px; margin: 30px auto; padding: 0 20px; display: flex; gap: 30px; align-items: flex-start; }
        .column { flex: 1; display: flex; flex-direction: column; gap: 25px; }
        .card { background: var(--card); border-radius: 16px; padding: 25px; border: 1px solid var(--border); }
        .card h2 { color: var(--primary); margin-bottom: 20px; padding-bottom: 12px; border-bottom: 2px dashed var(--border); }
        input, select { width: 100%; padding: 14px; margin: 8px 0; border-radius: 8px; border: 2px solid var(--border); background: var(--bg); color: var(--text); font-family: 'Outfit', sans-serif; font-size: 1rem; }
        input:focus, select:focus { outline: none; border-color: var(--primary); }
        input::placeholder { color: var(--muted); }
        .btn { width: 100%; padding: 14px; margin-top: 15px; border: none; border-radius: 8px; font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1rem; cursor: pointer; transition: 0.2s; }
        .btn:hover { opacity: 0.9; }
        .btn-primary { background: var(--primary); color: white; }
        .btn-accent { background: var(--accent); color: white; }
        .cat-item { font-weight: 800; font-size: 1.1rem; color: var(--primary); margin-top: 15px; }
        .menu-item { display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid var(--border); }
        .menu-item:last-child { border-bottom: none; }
    </style>
</head>
<body>
    <header>
        <h1>BITPOS</h1>
        <div class="nav-links">
            <a href="/sales/">Sales</a>
            <a href="/orders/">Orders</a>
            <a href="/menu/">Menu</a>
            <a href="/users/">Staff</a>
            <a href="/logout/" style="color:#E94560">Logout</a>
        </div>
    </header>
    <div class="container">
        <div class="column">
            <div class="card">
                <h2>Create Category</h2>
                <form method="POST">
                    {% csrf_token %}
                    <input type="hidden" name="action" value="add_category">
                    <input type="text" name="name" placeholder="Category Name (e.g. Hot Drinks)" required>
                    <button type="submit" class="btn btn-accent">Add Category</button>
                </form>
            </div>
            <div class="card">
                <h2>Create Menu Item</h2>
                <form method="POST">
                    {% csrf_token %}
                    <input type="hidden" name="action" value="add_item">
                    <select name="category" required>
                        <option value="">-- Select Category --</option>
                        {% for cat in categories %}
                        <option value="{{ cat.id }}">{{ cat.name }}</option>
                        {% endfor %}
                    </select>
                    <input type="text" name="name" placeholder="Item Name (e.g. Espresso)" required>
                    <input type="number" step="0.01" name="price" placeholder="Price (&#8377;)" required>
                    <button type="submit" class="btn btn-primary">Add Menu Item</button>
                </form>
            </div>
        </div>
        <div class="column">
            <div class="card">
                <h2>Current Menu</h2>
                {% for cat in categories %}
                <div class="cat-item">{{ cat.name }}</div>
                {% for item in cat.items.all %}
                <div class="menu-item">
                    <span>{{ item.name }}</span>
                    <span style="font-weight:800;color:var(--primary)">&#8377;{{ item.price }}</span>
                </div>
                {% empty %}
                <div class="menu-item" style="color:var(--muted)">No items yet</div>
                {% endfor %}
                {% empty %}
                <div style="text-align:center; padding:30px; color:var(--muted)">No categories yet</div>
                {% endfor %}
            </div>
        </div>
    </div>
</body>
</html>"""
with open('core/templates/core/manage_menu.html', 'w', encoding='utf-8') as f:
    f.write(manage_menu_html)


# Order Detail - Dark Theme
order_detail_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Order {{ order.order_number }} | BITPOS</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root { --bg: #1A1A2E; --card: #16213E; --primary: #D38C44; --accent: #0F3460; --text: #E8E8E8; --muted: #8892B0; --border: #233554; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Outfit', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }
        header { background: var(--card); padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--border); }
        h1 { font-weight: 800; font-size: 1.5rem; color: var(--primary); }
        .container { max-width: 700px; margin: 30px auto; padding: 0 20px; }
        .card { background: var(--card); border-radius: 16px; padding: 30px; border: 1px solid var(--border); margin-bottom: 20px; }
        .order-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px dashed var(--border); }
        .order-num { font-size: 1.5rem; font-weight: 800; color: var(--primary); }
        .meta-row { display: flex; justify-content: space-between; margin-bottom: 10px; }
        .meta-row span:first-child { color: var(--muted); }
        .meta-row span:last-child { font-weight: 800; }
        .items-table { width: 100%; margin: 20px 0; }
        .items-table th { text-align: left; padding: 10px 0; border-bottom: 2px solid var(--border); color: var(--muted); font-size: 0.85rem; text-transform: uppercase; }
        .items-table td { padding: 12px 0; border-bottom: 1px solid var(--border); }
        .total-row { display: flex; justify-content: space-between; font-size: 1.5rem; font-weight: 800; padding-top: 15px; margin-top: 10px; border-top: 2px dashed var(--border); }
        .btn { display: inline-block; padding: 12px 25px; background: var(--primary); color: white; border-radius: 8px; text-decoration: none; font-weight: 800; transition: 0.2s; }
        .btn:hover { opacity: 0.9; }
    </style>
</head>
<body>
    <header>
        <h1>BITPOS</h1>
        <a href="/orders/" style="color:var(--muted); text-decoration:none; font-weight:600;">Back to Orders</a>
    </header>
    <div class="container">
        <div class="card">
            <div class="order-header">
                <div class="order-num">{{ order.order_number }}</div>
                <div style="color:var(--muted)">{{ order.created_at|date:"d M Y, h:i A" }}</div>
            </div>
            <div class="meta-row"><span>Payment Method</span><span>{{ order.get_payment_method_display }}</span></div>
            <div class="meta-row"><span>Cash Amount</span><span>&#8377;{{ order.cash_amount }}</span></div>
            <div class="meta-row"><span>UPI Amount</span><span>&#8377;{{ order.upi_amount }}</span></div>
            <div class="meta-row"><span>Billed By</span><span>{{ order.billed_by.username|default:"--" }}</span></div>
            <table class="items-table">
                <tr><th>Item</th><th>Qty</th><th>Price</th><th>Total</th></tr>
                {% for item in items %}
                <tr>
                    <td style="font-weight:600">{{ item.item_name }}</td>
                    <td>{{ item.quantity }}</td>
                    <td>&#8377;{{ item.price }}</td>
                    <td style="font-weight:800; color:var(--primary)">&#8377;{{ item.price }}</td>
                </tr>
                {% endfor %}
            </table>
            <div class="total-row">
                <span>Total</span>
                <span style="color:var(--primary)">&#8377;{{ order.total_amount }}</span>
            </div>
        </div>
        <a href="/bill/{{ order.order_number }}/" class="btn" target="_blank">Print Bill</a>
    </div>
</body>
</html>"""
with open('core/templates/core/order_detail.html', 'w', encoding='utf-8') as f:
    f.write(order_detail_html)
