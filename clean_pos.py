path = 'core/templates/core/pos_dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Remove admin-only links from POS header since only users use it now
old_links = """            {% if request.user.profile.role == 'admin' %}
            <a href='/users/' style='color:inherit;text-decoration:none;margin-right:15px;padding:8px 12px;border:2px solid var(--border);border-radius:8px;transition:0.2s' onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">Staff</a>
            <a href='/menu/' style='color:inherit;text-decoration:none;margin-right:15px;padding:8px 12px;border:2px solid var(--border);border-radius:8px;transition:0.2s' onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">Menu</a>
            <a href='/orders/' style='color:inherit;text-decoration:none;margin-right:15px;padding:8px 12px;border:2px solid var(--border);border-radius:8px;transition:0.2s' onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">Orders</a>
            <a href='/sales/' style='color:inherit;text-decoration:none;margin-right:15px;padding:8px 12px;border:2px solid var(--border);border-radius:8px;transition:0.2s' onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">Sales</a>
            {% endif %}
            <span style='margin-right:20px'>Direct Sale Mode</span>"""

new_links = """            <span style='margin-right:20px'>Direct Sale Mode</span>"""

c = c.replace(old_links, new_links)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
