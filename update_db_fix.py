import os
import re
path = 'restaurant_pos/settings.py'
with open(path, 'r') as f:
    content = f.read()

# Fix imports
if 'import os' not in content:
    content = 'import os\n' + content

# Remove the messy DATABASES section and the extra brace
db_config = """
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        conn_max_age=600
    )
}
"""

# Replace the entire block from DATABASES until the next section
content = re.sub(r'DATABASES = \{.*?\}\n\n\}', db_config, content, flags=re.DOTALL)
# Also catch cases without the extra brace
content = re.sub(r'DATABASES = \{.*?\}', db_config, content, flags=re.DOTALL)

with open(path, 'w') as f:
    f.write(content)
print('Fixed settings.py syntax and imports')
