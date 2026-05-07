path = r'c:\Users\USER\.gemini\antigravity\brain\3d716617-f45f-4e94-861d-8537b1dcbb06\Django\restaurant_pos\restaurant_pos\settings.py'
with open(path, 'r') as f:
    content = f.read()

content = content.replace(\"'django.contrib.staticfiles',\", \"'django.contrib.staticfiles',\n    'core',\")

with open(path, 'w') as f:
    f.write(content)

path2 = r'c:\Users\USER\.gemini\antigravity\brain\3d716617-f45f-4e94-861d-8537b1dcbb06\Django\restaurant_pos\core\models.py'
models_content = '''from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(Category, related_name=\"items\", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Table(models.Model):
    table_number = models.CharField(max_length=10, unique=True)
    seating_capacity = models.IntegerField()
    is_occupied = models.BooleanField(default=False)
    
    def __str__(self):
        return f\"Table {self.table_number}\"

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('kot_sent', 'KOT Sent'),
        ('served', 'Served'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    )
    table = models.ForeignKey(Table, related_name=\"orders\", on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=\"pending\")
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f\"Order #{self.id} - {self.table}\"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name=\"items\", on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    special_instructions = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f\"{self.quantity}x {self.menu_item.name}\"
'''
with open(path2, 'w') as f:
    f.write(models_content)
