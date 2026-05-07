import os

path = 'core/templates/core/pos_dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

old_header_content = "<div style='font-weight: 600; color: #8A7A6F;'>Direct Sale Mode <a href='/logout/' style='color:#C96459;text-decoration:none;margin-left:20px;font-weight:800'>Logout</a></div>"
new_header_content = """<div style='font-weight: 600; color: #8A7A6F;'>
            <a href='/users/' style='color:inherit;text-decoration:none;margin-right:20px'>Manage Staff</a>
            <a href='/menu/' style='color:inherit;text-decoration:none;margin-right:20px'>Manage Menu</a>
            Direct Sale Mode 
            <a href='/logout/' style='color:#C96459;text-decoration:none;margin-left:20px;font-weight:800'>Logout</a>
        </div>"""

if old_header_content in c:
    c = c.replace(old_header_content, new_header_content)
else:
    # Fallback if old header was slightly different
    old_div = "<div style='font-weight: 600; color: #8A7A6F;'>Direct Sale Mode</div>"
    if old_div in c:
        c = c.replace(old_div, new_header_content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
