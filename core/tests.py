from django.test import TestCase
from .models import Company, Category, MenuItem, Table, Order, OrderItem, UserProfile
from django.contrib.auth.models import User

class CoreModelTests(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Test Company', address='123 Test St')
        self.category = Category.objects.create(company=self.company, name='Drinks')
        self.menu_item = MenuItem.objects.create(company=self.company, category=self.category, name='Cola', price=1.99)
        self.table = Table.objects.create(company=self.company, table_number='A1', seating_capacity=2)
        self.user = User.objects.create_user(username='testadmin', password='password123')
        self.profile = UserProfile.objects.create(user=self.user, company=self.company, role='admin')

    def test_company_creation(self):
        self.assertEqual(self.company.name, 'Test Company')
        self.assertEqual(str(self.company), 'Test Company')

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Drinks')
        self.assertEqual(str(self.category), 'Drinks (Test Company)')

    def test_menu_item_creation(self):
        self.assertEqual(self.menu_item.price, 1.99)
        self.assertEqual(str(self.menu_item), 'Cola')

    def test_order_and_order_item(self):
        order = Order.objects.create(company=self.company, table=self.table, billed_by=self.user)
        self.assertTrue(order.order_number.startswith('ORD-'))
        
        order_item = OrderItem.objects.create(order=order, menu_item=self.menu_item, price=self.menu_item.price)
        self.assertEqual(order_item.item_name, 'Cola')
        self.assertEqual(str(order_item), '1x Cola')

    def test_user_profile(self):
        self.assertEqual(self.profile.role, 'admin')
