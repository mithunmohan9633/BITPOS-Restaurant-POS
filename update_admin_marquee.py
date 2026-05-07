path = 'core/templates/core/sales_dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Add marquee styles
marquee_style = """        .marquee-container {
            background: #FFD700;
            color: #1A1A2E;
            padding: 10px 0;
            font-weight: 800;
            overflow: hidden;
            white-space: nowrap;
            position: relative;
            margin-bottom: 20px;
            border-radius: 8px;
        }
        .marquee-text {
            display: inline-block;
            padding-left: 100%;
            animation: marquee 20s linear infinite;
        }
        @keyframes marquee {
            0% { transform: translate(0, 0); }
            100% { transform: translate(-100%, 0); }
        }"""

c = c.replace(":root {", marquee_style + "\n        :root {")

# Add marquee element right after header
marquee_html = """    </header>
    {% if expiry_warning %}
    <div class="container" style="margin-top: 20px; margin-bottom: 0;">
        <div class="marquee-container">
            <div class="marquee-text">
                🚨 IMPORTANT: Your subscription is expiring in {{ days_left }} days! Please contact support to renew your plan and avoid service interruption. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 🚨 IMPORTANT: Your subscription is expiring in {{ days_left }} days! Please contact support to renew your plan and avoid service interruption.
            </div>
        </div>
    </div>
    {% endif %}"""

c = c.replace("</header>", marquee_html)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("Updated sales_dashboard.html")
