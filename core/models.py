from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import random
import string

class Company(models.Model):
    plan_name = models.CharField(max_length=50, default='Standard')
    valid_until = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    POS_CHOICES = (('restaurant', 'Restaurant POS'), ('cafe', 'Cafe POS'))
    pos_type = models.CharField(max_length=20, choices=POS_CHOICES, default='restaurant')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Printer(models.Model):
    PRINTER_TYPE_CHOICES = (
        ('cash_bill', 'Cash / Bill Printer'),
        ('kot', 'KOT Kitchen/Station Printer'),
    )
    company = models.ForeignKey(Company, related_name='printers', on_delete=models.CASCADE)
    name = models.CharField(max_length=100) # e.g. CASH, KITCHEN, JUICE
    printer_type = models.CharField(max_length=20, choices=PRINTER_TYPE_CHOICES, default='kot')
    ip_address = models.CharField(max_length=50, default='192.168.1.100')
    port = models.IntegerField(default=9100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.ip_address}:{self.port}) - {self.get_printer_type_display()}"

class Category(models.Model):
    company = models.ForeignKey(Company, related_name='categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    printer = models.ForeignKey(Printer, related_name='categories', on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f'{self.name} ({self.company.name})'

class MenuItem(models.Model):
    company = models.ForeignKey(Company, related_name='menu_items', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    image = models.ImageField(upload_to='menu_items/', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Table(models.Model):
    company = models.ForeignKey(Company, related_name='tables', on_delete=models.CASCADE)
    table_number = models.CharField(max_length=10)
    seating_capacity = models.IntegerField()
    is_occupied = models.BooleanField(default=False)
    def __str__(self):
        return f'Table {self.table_number} ({self.company.name})'

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('invoiced', 'Invoiced'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    )
    PAYMENT_CHOICES = (
        ('cash', 'Cash'),
        ('card', 'Card / Online'),
        ('split', 'Split (Cash + Card)'),
    )
    company = models.ForeignKey(Company, related_name='orders', on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    table = models.ForeignKey(Table, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cash')
    cash_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    upi_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_type = models.CharField(max_length=20, default='dine_in')
    billed_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            prefix = 'ORD'
            rand = ''.join(random.choices(string.digits, k=6))
            self.order_number = f'{prefix}-{rand}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order #{self.order_number}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200, blank=True)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    special_instructions = models.TextField(blank=True, null=True)
    is_printed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.item_name and self.menu_item:
            self.item_name = self.menu_item.name
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.quantity}x {self.item_name}'

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    ROLE_CHOICES = (
        ('admin', 'Store Admin'),
        ('cashier_restaurant', 'Restaurant Cashier'),
        ('cashier_cafe', 'Cafe Cashier'),
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='cashier_restaurant')

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

class Expense(models.Model):
    company = models.ForeignKey(Company, related_name='expenses', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"
