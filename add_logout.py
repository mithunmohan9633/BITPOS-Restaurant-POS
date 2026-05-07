import os

files = [
    'core/templates/core/pos_dashboard.html',
    'core/templates/core/manage_users.html',
    'core/templates/core/manage_menu.html'
]

logout_link = "<a href='/logout/' style='color:#C96459;text-decoration:none;margin-left:20px;font-weight:800'>Logout</a>"

for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "</div>\n    </header>" in content:
        content = content.replace("</div>\n    </header>", f" {logout_link}</div>\n    </header>")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
