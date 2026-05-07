import os
import re
path = 'restaurant_pos/settings.py'
with open(path, 'r') as f:
    content = f.read()

if 'import dj_database_url' not in content:
    content = 'import dj_database_url\n' + content

db_config = """
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        conn_max_age=600
    )
}
"""

content = re.sub(r'DATABASES = \{.*?\}', db_config, content, flags=re.DOTALL)

with open(path, 'w') as f:
    f.write(content)
print('Updated settings.py for PostgreSQL')
