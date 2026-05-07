import os
import django

models_append = """
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    ROLE_CHOICES = (
        ('admin', 'Store Admin'),
        ('cashier_restaurant', 'Restaurant Cashier'),
        ('cashier_retail', 'Retail Cashier'),
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='cashier_restaurant')

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
"""

with open('core/models.py', 'a', encoding='utf-8') as f:
    f.write(models_append)

admin_code = """from django.contrib import admin
from .models import Company, Category, MenuItem, Table, Order, OrderItem, UserProfile

admin.site.register(Company)
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Table)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(UserProfile)
"""

with open('core/admin.py', 'w', encoding='utf-8') as f:
    f.write(admin_code)
