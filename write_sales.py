# Sales Analytics Dashboard
sales_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sales Dashboard | BITPOS</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root { --bg: #1A1A2E; --card: #16213E; --primary: #D38C44; --accent: #0F3460; --text: #E8E8E8; --muted: #8892B0; --success: #4ECB71; --purple: #6366F1; --border: #233554; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Outfit', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }
        header { background: var(--card); padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--border); }
        h1 { font-weight: 800; font-size: 1.5rem; }
        .nav-links a { color: var(--muted); text-decoration: none; margin-left: 20px; font-weight: 600; }
        .nav-links a:hover { color: var(--primary); }
        .container { max-width: 1200px; margin: 30px auto; padding: 0 20px; }

        .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: var(--card); border-radius: 12px; padding: 25px; border: 1px solid var(--border); }
        .stat-label { color: var(--muted); font-weight: 600; font-size: 0.85rem; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }
        .stat-value { font-size: 2rem; font-weight: 800; }
        .stat-sub { color: var(--muted); font-size: 0.85rem; margin-top: 5px; }

        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin-bottom: 30px; }
        .card { background: var(--card); border-radius: 16px; padding: 25px; border: 1px solid var(--border); }
        .card h2 { font-weight: 800; margin-bottom: 20px; font-size: 1.2rem; color: var(--primary); }

        .payment-bars { display: flex; flex-direction: column; gap: 15px; }
        .pay-row { display: flex; align-items: center; gap: 15px; }
        .pay-label { min-width: 80px; font-weight: 800; font-size: 0.9rem; }
        .pay-bar-bg { flex: 1; height: 30px; background: var(--border); border-radius: 8px; overflow: hidden; }
        .pay-bar { height: 100%; border-radius: 8px; display: flex; align-items: center; padding-left: 10px; font-weight: 800; font-size: 0.8rem; color: white; transition: width 0.5s; }
        .pay-bar-cash { background: var(--success); }
        .pay-bar-upi { background: var(--purple); }
        .pay-amount { min-width: 100px; text-align: right; font-weight: 800; }

        .product-table { width: 100%; }
        .product-row { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid var(--border); }
        .product-row:last-child { border-bottom: none; }
        .product-name { font-weight: 600; }
        .product-qty { color: var(--muted); font-weight: 800; }
        .product-rev { color: var(--primary); font-weight: 800; }

        .chart-container { position: relative; height: 250px; }
    </style>
</head>
<body>
    <header>
        <h1>BITPOS - Sales Analytics</h1>
        <div class="nav-links">
            <a href="/">POS</a>
            <a href="/orders/">Orders</a>
            <a href="/menu/">Menu</a>
            <a href="/users/">Staff</a>
            <a href="/logout/" style="color:#E94560">Logout</a>
        </div>
    </header>
    <div class="container">
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Today's Sales</div>
                <div class="stat-value" style="color: var(--success)">&#8377;{{ today_total }}</div>
                <div class="stat-sub">{{ today_count }} orders</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">This Month</div>
                <div class="stat-value" style="color: var(--primary)">&#8377;{{ month_total }}</div>
                <div class="stat-sub">{{ month_count }} orders</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">This Year</div>
                <div class="stat-value" style="color: var(--purple)">&#8377;{{ year_total }}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">All Time</div>
                <div class="stat-value" style="color: var(--text)">&#8377;{{ all_time_total }}</div>
            </div>
        </div>

        <div class="grid-2">
            <div class="card">
                <h2>Last 7 Days Revenue</h2>
                <div class="chart-container">
                    <canvas id="dailyChart"></canvas>
                </div>
            </div>

            <div class="card">
                <h2>Payment Breakdown (Today)</h2>
                <div class="payment-bars" style="margin-top: 30px;">
                    <div class="pay-row">
                        <span class="pay-label" style="color: var(--success)">Cash</span>
                        <div class="pay-bar-bg"><div class="pay-bar pay-bar-cash" id="cash-bar"></div></div>
                        <span class="pay-amount" style="color: var(--success)">&#8377;{{ today_cash }}</span>
                    </div>
                    <div class="pay-row">
                        <span class="pay-label" style="color: var(--purple)">UPI</span>
                        <div class="pay-bar-bg"><div class="pay-bar pay-bar-upi" id="upi-bar"></div></div>
                        <span class="pay-amount" style="color: var(--purple)">&#8377;{{ today_upi }}</span>
                    </div>
                    <div style="margin-top:20px; padding-top:15px; border-top:1px solid var(--border)">
                        <h2 style="font-size:1rem; margin-bottom:15px;">Payment Breakdown (Month)</h2>
                        <div class="pay-row">
                            <span class="pay-label" style="color: var(--success)">Cash</span>
                            <div class="pay-bar-bg"><div class="pay-bar pay-bar-cash" id="mcash-bar"></div></div>
                            <span class="pay-amount" style="color: var(--success)">&#8377;{{ month_cash }}</span>
                        </div>
                        <div class="pay-row" style="margin-top:10px">
                            <span class="pay-label" style="color: var(--purple)">UPI</span>
                            <div class="pay-bar-bg"><div class="pay-bar pay-bar-upi" id="mupi-bar"></div></div>
                            <span class="pay-amount" style="color: var(--purple)">&#8377;{{ month_upi }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>Product-wise Sales (All Time)</h2>
            <div class="product-table">
                {% for p in product_sales %}
                <div class="product-row">
                    <span class="product-name">{{ p.item_name }}</span>
                    <span class="product-qty">{{ p.total_qty }} sold</span>
                    <span class="product-rev">&#8377;{{ p.total_revenue }}</span>
                </div>
                {% empty %}
                <div style="text-align:center; padding:30px; color:var(--muted)">No sales data yet</div>
                {% endfor %}
            </div>
        </div>
    </div>

    <script>
        // Daily Chart
        var ctx = document.getElementById('dailyChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: {{ daily_labels|safe }},
                datasets: [{
                    label: 'Revenue',
                    data: {{ daily_data|safe }},
                    backgroundColor: 'rgba(211, 140, 68, 0.7)',
                    borderColor: '#D38C44',
                    borderWidth: 2,
                    borderRadius: 6,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { ticks: { color: '#8892B0' }, grid: { color: '#233554' } },
                    x: { ticks: { color: '#8892B0' }, grid: { display: false } }
                }
            }
        });

        // Payment bars animation
        setTimeout(function() {
            var todayCash = {{ today_cash }};
            var todayUpi = {{ today_upi }};
            var todayTotal = todayCash + todayUpi;
            if (todayTotal > 0) {
                document.getElementById('cash-bar').style.width = (todayCash / todayTotal * 100) + '%';
                document.getElementById('upi-bar').style.width = (todayUpi / todayTotal * 100) + '%';
            }
            var monthCash = {{ month_cash }};
            var monthUpi = {{ month_upi }};
            var monthTotal = monthCash + monthUpi;
            if (monthTotal > 0) {
                document.getElementById('mcash-bar').style.width = (monthCash / monthTotal * 100) + '%';
                document.getElementById('mupi-bar').style.width = (monthUpi / monthTotal * 100) + '%';
            }
        }, 300);
    </script>
</body>
</html>"""
with open('core/templates/core/sales_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(sales_html)
