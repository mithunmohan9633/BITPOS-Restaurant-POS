import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_pos.settings')
django.setup()

from core.models import Company, Category, MenuItem, Table, UserProfile
from django.contrib.auth.models import User

company, _ = Company.objects.get_or_create(name='Awesome Bites', address='123 Food Street')

user, created = User.objects.get_or_create(username='admin')
if created:
    user.set_password('admin123')
    user.save()
UserProfile.objects.get_or_create(user=user, company=company, role='admin')

cashier, created = User.objects.get_or_create(username='cashier')
if created:
    cashier.set_password('cashier123')
    cashier.save()
UserProfile.objects.get_or_create(user=cashier, company=company, role='cashier_restaurant')

cat1, _ = Category.objects.get_or_create(company=company, name='Starters')
cat2, _ = Category.objects.get_or_create(company=company, name='Main Course')

MenuItem.objects.get_or_create(company=company, category=cat1, name='Spring Rolls', price=5.99)
MenuItem.objects.get_or_create(company=company, category=cat2, name='Grilled Chicken', price=12.99)

Table.objects.get_or_create(company=company, table_number='T1', seating_capacity=4)
Table.objects.get_or_create(company=company, table_number='T2', seating_capacity=2)

print('Data seeded successfully!')
