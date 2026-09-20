import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_pos.settings')
django.setup()
from django.contrib.auth.models import User
from core.models import UserProfile, Company

for user in User.objects.all():
    try:
        profile = user.profile
        print(f"User: {user.username} | Role: {profile.role} | Company: {profile.company}")
    except Exception as e:
        print(f"User: {user.username} | No profile! Error: {e}")
