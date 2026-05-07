# Order History Page
order_history_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Order History | BITPOS</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root { --bg-color: #FDF8F5; --card-bg: #FFFFFF; --text-color: #4A3B32; --primary: #D38C44; --border: #E8DCCB; }
        body { margin: 0; font-family: 'Outfit', sans-serif; background: var(--bg-color); color: var(--text-color); }
        header { padding: 15px 30px; background: var(--card-bg); border-bottom: 2px solid var(--border); display: flex; justify-content: space-between; align-items: center; }
        h1 { margin: 0; font-weight: 800; font-size: 1.5rem; }
        .container { max-width: 1000px; margin: 30px auto; padding: 0 20px; }
        .search-bar { display: flex; gap: 10px; margin-bottom: 25px; }
        .search-bar input { flex: 1; padding: 14px; border-radius: 8px; border: 2px solid var(--border); font-family: 'Outfit', sans-serif; font-size: 1rem; }
        .search-bar input:focus { outline: none; border-color: var(--primary); }
        .search-bar button { padding: 14px 25px; background: var(--primary); color: white; border: none; border-radius: 8px; font-weight: 800; cursor: pointer; }
        table { width: 100%; border-collapse: collapse; background: var(--card-bg); border-radius: 12px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
        th { background: var(--primary); color: white; text-align: left; padding: 15px 20px; font-weight: 800; font-size: 0.85rem; letter-spacing: 1px; text-transform: uppercase; }
        td { padding: 15px 20px; border-bottom: 1px solid var(--border); }
        tr:last-child td { border-bottom: none; }
        tr:hover { background: #FFF9F8; }
        .order-link { color: var(--primary); font-weight: 800; text-decoration: none; }
        .order-link:hover { text-decoration: underline; }
        .badge { padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 800; }
        .badge-cash { background: rgba(78,203,113,0.15); color: #4ECB71; }
        .badge-upi { background: rgba(99,102,241,0.15); color: #6366F1; }
        .badge-split { background: rgba(211,140,68,0.15); color: #D38C44; }
        .nav-links a { color: #8A7A6F; text-decoration: none; margin-left: 20px; font-weight: 600; }
        .nav-links a:hover { color: var(--primary); }
    </style>
</head>
<body>
    <header>
        <h1>BITPOS</h1>
        <div class="nav-links">
            <a href="/">POS</a>
            <a href="/sales/">Sales</a>
            <a href="/menu/">Menu</a>
            <a href="/users/">Staff</a>
            <a href="/logout/" style="color:#C96459">Logout</a>
        </div>
    </header>
    <div class="container">
        <h2 style="margin-bottom: 20px;">Order History</h2>
        <form class="search-bar" method="GET">
            <input type="text" name="search" placeholder="Search by Order Number..." value="{{ search }}">
            <button type="submit">Search</button>
        </form>
        <table>
            <tr>
                <th>Order #</th>
                <th>Date & Time</th>
                <th>Amount</th>
                <th>Payment</th>
                <th>Billed By</th>
                <th>Actions</th>
            </tr>
            {% for order in orders %}
            <tr>
                <td><a href="/orders/{{ order.order_number }}/" class="order-link">{{ order.order_number }}</a></td>
                <td>{{ order.created_at|date:"d M Y, h:i A" }}</td>
                <td style="font-weight:800; color:var(--primary)">&#8377;{{ order.total_amount }}</td>
                <td>
                    <span class="badge {% if order.payment_method == 'cash' %}badge-cash{% elif order.payment_method == 'upi' %}badge-upi{% else %}badge-split{% endif %}">
                        {{ order.get_payment_method_display }}
                    </span>
                </td>
                <td>{{ order.billed_by.username|default:"--" }}</td>
                <td><a href="/bill/{{ order.order_number }}/" class="order-link" target="_blank">View Bill</a></td>
            </tr>
            {% empty %}
            <tr><td colspan="6" style="text-align:center; padding:40px; color:#8A7A6F">No orders found</td></tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>"""
with open('core/templates/core/order_history.html', 'w', encoding='utf-8') as f:
    f.write(order_history_html)


# Order Detail Page
order_detail_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Order {{ order.order_number }} | BITPOS</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root { --bg-color: #FDF8F5; --card-bg: #FFFFFF; --text-color: #4A3B32; --primary: #D38C44; --border: #E8DCCB; }
        body { margin: 0; font-family: 'Outfit', sans-serif; background: var(--bg-color); color: var(--text-color); }
        header { padding: 15px 30px; background: var(--card-bg); border-bottom: 2px solid var(--border); display: flex; justify-content: space-between; align-items: center; }
        h1 { margin: 0; font-weight: 800; font-size: 1.5rem; }
        .container { max-width: 700px; margin: 30px auto; padding: 0 20px; }
        .card { background: var(--card-bg); border-radius: 16px; padding: 30px; border: 2px solid var(--border); box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px; }
        .order-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px dashed var(--border); }
        .order-num { font-size: 1.5rem; font-weight: 800; color: var(--primary); }
        .meta-row { display: flex; justify-content: space-between; margin-bottom: 10px; color: #8A7A6F; }
        .meta-row span:last-child { font-weight: 800; color: var(--text-color); }
        .items-table { width: 100%; margin: 20px 0; }
        .items-table th { text-align: left; padding: 10px 0; border-bottom: 2px solid var(--border); color: #8A7A6F; font-size: 0.85rem; text-transform: uppercase; }
        .items-table td { padding: 12px 0; border-bottom: 1px solid var(--border); }
        .total-row { display: flex; justify-content: space-between; font-size: 1.5rem; font-weight: 800; padding-top: 15px; margin-top: 10px; border-top: 2px dashed var(--border); }
        .btn { display: inline-block; padding: 12px 25px; background: var(--primary); color: white; border-radius: 8px; text-decoration: none; font-weight: 800; }
    </style>
</head>
<body>
    <header>
        <h1>BITPOS</h1>
        <a href="/orders/" style="color:#8A7A6F; text-decoration:none; font-weight:600;">Back to Orders</a>
    </header>
    <div class="container">
        <div class="card">
            <div class="order-header">
                <div class="order-num">{{ order.order_number }}</div>
                <div style="color:#8A7A6F">{{ order.created_at|date:"d M Y, h:i A" }}</div>
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
                    <td style="font-weight:800; color:var(--primary)">&#8377;{{ item.price|floatformat:2 }}</td>
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
