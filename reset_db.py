import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_pos.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User
from core.models import UserProfile

call_command('flush', interactive=False)

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')

print("Database flushed and superuser created.")
