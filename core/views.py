
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Company, Category, MenuItem, UserProfile, Printer, Table
from .printer_service import print_kot_for_order, print_bill_for_order, test_printer, print_table_transfer_notice
import re

def validate_credentials(username, password=None):
    errors = []
    if not re.match(r'^[a-z0-9]+$', username):
        errors.append("Username must be alphanumeric and lowercase only.")
    if password:
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', password):
            errors.append("Password must contain at least one number.")
        if not re.search(r'[^A-Za-z0-9]', password):
            errors.append("Password must contain at least one special character.")
    return errors


def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return HttpResponseRedirect(reverse('super_admin_dashboard'))
            elif hasattr(user, 'profile') and user.profile.role == 'admin':
                return HttpResponseRedirect(reverse('sales_dashboard'))
            else:
                return HttpResponseRedirect(reverse('pos_dashboard'))
        else:
            return render(request, 'core/login.html', {'error': 'Invalid username or password'})
    return render(request, 'core/login.html')


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_view'))


@login_required(login_url='login_view')
def super_admin_dashboard(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Access Denied: Super Admin only.")
    companies = Company.objects.all().order_by('-created_at')
    admins = UserProfile.objects.filter(role='admin').select_related('user', 'company')
    active_count = companies.filter(is_active=True).count()
    return render(request, 'core/super_admin.html', {
        'companies': companies,
        'admins': admins,
        'active_count': active_count,
    })


@login_required(login_url='login_view')
def super_admin_create_company(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Access Denied.")
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        address = request.POST.get('address', '')
        pos_type = request.POST.get('pos_type', 'restaurant')
        plan_name = request.POST.get('plan_name', 'Standard')
        valid_until = request.POST.get('valid_until')
        if name:
            existing = Company.objects.filter(name__iexact=name).first()
            if existing:
                # Block duplicate registration — show clear error
                messages.error(request, f"A company named '{existing.name}' already exists! Use the Edit button on the existing company to update its details.")
            else:
                company = Company(name=name, address=address, pos_type=pos_type, plan_name=plan_name)
                if valid_until:
                    company.valid_until = valid_until
                company.save()
                messages.success(request, f"Company '{name}' registered successfully.")
    return HttpResponseRedirect(reverse('super_admin_dashboard'))




@login_required(login_url='login_view')
def super_admin_edit_company(request, company_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden('Access Denied.')
    if request.method == 'POST':
        try:
            company = Company.objects.get(id=company_id)
            company.name = request.POST.get('name', company.name)
            company.address = request.POST.get('address', company.address)
            company.pos_type = request.POST.get('pos_type', company.pos_type)
            company.plan_name = request.POST.get('plan_name', company.plan_name)
            valid_until = request.POST.get('valid_until')
            if valid_until:
                company.valid_until = valid_until
            company.save()
            messages.success(request, 'Company updated successfully.')
        except Company.DoesNotExist:
            messages.error(request, 'Company not found.')
    return HttpResponseRedirect(reverse('super_admin_dashboard'))


@login_required(login_url='login_view')
def super_admin_delete_company(request, company_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden('Access Denied.')
    if request.method == 'POST':
        try:
            company = Company.objects.get(id=company_id)
            # Get all users linked to this company via UserProfile and delete them
            # (CASCADE deletes profile, but not the auth User itself)
            user_ids = UserProfile.objects.filter(company=company).values_list('user_id', flat=True)
            User.objects.filter(id__in=user_ids).delete()
            # Now delete the company — cascades to Category, MenuItem, Table, Order, OrderItem
            company.delete()
            messages.success(request, 'Company and all related data (users, menu, orders) removed successfully.')
        except Company.DoesNotExist:
            messages.error(request, 'Company not found.')
    return HttpResponseRedirect(reverse('super_admin_dashboard'))


@login_required(login_url='login_view')
def super_admin_create_admin(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Access Denied.")
    if request.method == 'POST':
        action = request.POST.get('action', 'add')
        if action == 'add':
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password')
            company_id = request.POST.get('company')
            if username and password and company_id:
                errors = validate_credentials(username, password)
                if errors:
                    for error in errors:
                        messages.error(request, error)
                # Check 1: Username must be unique
                elif User.objects.filter(username=username).exists():
                    messages.error(request, f"Username '{username}' is already taken. Please choose a different username.")
                # Check 2: Company must not already have an admin
                elif UserProfile.objects.filter(company_id=company_id, role='admin').exists():
                    existing_admin = UserProfile.objects.get(company_id=company_id, role='admin')
                    messages.error(request, f"Company already has an admin '{existing_admin.user.username}'. Edit the existing admin or remove them first.")
                else:
                    user = User.objects.create_user(username=username, password=password)
                    company = Company.objects.get(id=company_id)
                    UserProfile.objects.create(user=user, role='admin', company=company)
                    messages.success(request, f"Admin '{username}' created successfully for {company.name}.")
        elif action == 'edit':
            user_id = request.POST.get('user_id')
            username = request.POST.get('username')
            password = request.POST.get('password')
            company_id = request.POST.get('company')
            if user_id and username and company_id:
                errors = validate_credentials(username, password if password else None)
                if errors:
                    for error in errors:
                        messages.error(request, error)
                else:
                    try:
                        user = User.objects.get(id=user_id, profile__role='admin')
                        if User.objects.filter(username=username).exclude(id=user_id).exists():
                            messages.error(request, 'Username already taken.')
                        elif UserProfile.objects.filter(company_id=company_id, role='admin').exclude(user_id=user_id).exists():
                            existing_admin = UserProfile.objects.get(company_id=company_id, role='admin').user.username
                            messages.error(request, f"Company already has an admin '{existing_admin}'.")
                        else:
                            user.username = username
                            if password:
                                user.set_password(password)
                            user.save()
                            company = Company.objects.get(id=company_id)
                            user.profile.company = company
                            user.profile.save()
                            messages.success(request, 'Admin user updated successfully.')
                    except Exception as e:
                        messages.error(request, 'Error updating admin user.')
        elif action == 'delete':
            user_id = request.POST.get('user_id')
            if user_id:
                try:
                    user = User.objects.get(id=user_id, profile__role='admin')
                    user.delete()
                    messages.success(request, 'Admin user deleted successfully.')
                except Exception as e:
                    messages.error(request, 'Error deleting admin user.')
    return HttpResponseRedirect(reverse('super_admin_dashboard'))


@login_required(login_url='login_view')
def super_admin_toggle_company(request, company_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Access Denied.")
    company = Company.objects.get(id=company_id)
    company.is_active = not company.is_active
    company.save()
    return HttpResponseRedirect(reverse('super_admin_dashboard'))


@login_required(login_url='login_view')
def pos_dashboard(request):
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('super_admin_dashboard'))
    if not hasattr(request.user, 'profile') or not request.user.profile.company:
        return HttpResponseForbidden("Your account is not assigned to any store.")
    if request.user.profile.role == 'admin':
        return HttpResponseRedirect(reverse('sales_dashboard'))
    company = request.user.profile.company
    from .models import Table
    tables = Table.objects.filter(company=company).order_by('table_number')
    categories = Category.objects.filter(company=company).prefetch_related('items')
    return render(request, 'core/pos_dashboard.html', {
        'categories': categories,
        'tables': tables,
        'company': company,
    })

@login_required(login_url='login_view')
def manage_users(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        return HttpResponseForbidden("Access Denied: Only Store Admins can manage users.")
    company = request.user.profile.company
    if request.method == 'POST':
        action = request.POST.get('action', 'add')
        if action == 'add':
            username = request.POST.get('username')
            password = request.POST.get('password')
            role = request.POST.get('role')
            if username and password:
                errors = validate_credentials(username, password)
                if errors:
                    for error in errors:
                        messages.error(request, error)
                elif not User.objects.filter(username=username).exists():
                    user = User.objects.create_user(username=username, password=password)
                    UserProfile.objects.create(user=user, role=role, company=company)
                    messages.success(request, 'User added successfully.')
                else:
                    messages.error(request, 'User already exists.')
        elif action == 'edit':
            user_id = request.POST.get('user_id')
            username = request.POST.get('username')
            password = request.POST.get('password')
            role = request.POST.get('role')
            if user_id and username:
                errors = validate_credentials(username, password if password else None)
                if errors:
                    for error in errors:
                        messages.error(request, error)
                else:
                    try:
                        user = User.objects.get(id=user_id, profile__company=company)
                        if User.objects.filter(username=username).exclude(id=user_id).exists():
                            messages.error(request, 'Username already taken.')
                        else:
                            user.username = username
                            if password:
                                user.set_password(password)
                            user.save()
                            if hasattr(user, 'profile'):
                                user.profile.role = role
                                user.profile.save()
                            messages.success(request, 'User updated successfully.')
                    except Exception as e:
                        messages.error(request, 'Error updating user.')
        elif action == 'delete':
            user_id = request.POST.get('user_id')
            if user_id:
                try:
                    user = User.objects.get(id=user_id, profile__company=company)
                    user.delete()
                    messages.success(request, 'User deleted successfully.')
                except Exception as e:
                    messages.error(request, 'Error deleting user.')
        return HttpResponseRedirect(reverse('manage_users'))
    profiles = UserProfile.objects.filter(company=company)
    return render(request, 'core/manage_users.html', {'profiles': profiles})


@login_required(login_url='login_view')
def manage_printers(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        return HttpResponseForbidden("Access Denied: Only Store Admins can manage printers.")
    company = request.user.profile.company
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_printer':
            name = request.POST.get('name', '').strip().upper()
            printer_type = request.POST.get('printer_type', 'kot')
            ip_address = request.POST.get('ip_address', '').strip()
            port = int(request.POST.get('port', 9100) or 9100)
            if name and ip_address:
                Printer.objects.create(
                    company=company,
                    name=name,
                    printer_type=printer_type,
                    ip_address=ip_address,
                    port=port,
                    is_active=True
                )
                messages.success(request, f"Printer '{name}' added successfully.")
        elif action == 'edit_printer':
            printer_id = request.POST.get('printer_id')
            name = request.POST.get('name', '').strip().upper()
            printer_type = request.POST.get('printer_type', 'kot')
            ip_address = request.POST.get('ip_address', '').strip()
            port = int(request.POST.get('port', 9100) or 9100)
            is_active = request.POST.get('is_active') == 'on'
            if printer_id and name and ip_address:
                try:
                    p = Printer.objects.get(id=printer_id, company=company)
                    p.name = name
                    p.printer_type = printer_type
                    p.ip_address = ip_address
                    p.port = port
                    p.is_active = is_active
                    p.save()
                    messages.success(request, f"Printer '{name}' updated successfully.")
                except Printer.DoesNotExist:
                    messages.error(request, "Printer not found.")
        elif action == 'delete_printer':
            printer_id = request.POST.get('printer_id')
            if printer_id:
                try:
                    p = Printer.objects.get(id=printer_id, company=company)
                    p.delete()
                    messages.success(request, "Printer deleted successfully.")
                except Printer.DoesNotExist:
                    messages.error(request, "Printer not found.")
        elif action == 'map_category':
            cat_id = request.POST.get('category_id')
            printer_id = request.POST.get('printer_id')
            if cat_id:
                try:
                    cat = Category.objects.get(id=cat_id, company=company)
                    if printer_id:
                        cat.printer = Printer.objects.get(id=printer_id, company=company)
                    else:
                        cat.printer = None
                    cat.save()
                    messages.success(request, f"Category '{cat.name}' assigned to {cat.printer.name if cat.printer else 'None'}.")
                except Exception:
                    messages.error(request, "Error assigning category to printer.")
        return HttpResponseRedirect(reverse('manage_printers'))

    printers = Printer.objects.filter(company=company).order_by('printer_type', 'name')
    categories = Category.objects.filter(company=company).select_related('printer')
    kot_printers = printers.filter(printer_type='kot')
    return render(request, 'core/manage_printers.html', {
        'printers': printers,
        'categories': categories,
        'kot_printers': kot_printers,
        'company': company
    })


@login_required(login_url='login_view')
def manage_menu(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        return HttpResponseForbidden("Access Denied: Only Store Admins can manage the menu.")
    company = request.user.profile.company
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_category':
            name = request.POST.get('name')
            printer_id = request.POST.get('printer')
            if name:
                if Category.objects.filter(company=company, name__iexact=name).exists():
                    messages.error(request, f"A category with the name '{name}' already exists.")
                else:
                    printer = Printer.objects.filter(id=printer_id, company=company).first() if printer_id else None
                    Category.objects.create(name=name, company=company, printer=printer)
                    messages.success(request, "Category added successfully.")
        elif action == 'edit_category':
            cat_id = request.POST.get('category_id')
            name = request.POST.get('name')
            printer_id = request.POST.get('printer')
            if cat_id and name:
                try:
                    cat = Category.objects.get(id=cat_id, company=company)
                    cat.name = name
                    cat.printer = Printer.objects.filter(id=printer_id, company=company).first() if printer_id else None
                    cat.save()
                    messages.success(request, "Category updated successfully.")
                except Category.DoesNotExist:
                    pass
        elif action == 'delete_category':
            cat_id = request.POST.get('category_id')
            if cat_id:
                try:
                    Category.objects.filter(id=cat_id, company=company).delete()
                    messages.success(request, "Category deleted successfully.")
                except Exception:
                    pass
        elif action == 'add_item':
            category_id = request.POST.get('category')
            name = request.POST.get('name')
            price = request.POST.get('price')
            image = request.FILES.get('image')
            if name and price and category_id:
                if MenuItem.objects.filter(company=company, name__iexact=name).exists():
                    messages.error(request, f"A product with the name '{name}' already exists.")
                else:
                    category = Category.objects.get(id=category_id, company=company)
                    MenuItem.objects.create(name=name, price=price, category=category, company=company, image=image)
                    messages.success(request, "Product added successfully.")
        elif action == 'edit_item':
            item_id = request.POST.get('item_id')
            category_id = request.POST.get('category')
            name = request.POST.get('name')
            price = request.POST.get('price')
            image = request.FILES.get('image')
            if item_id and name and price and category_id:
                if MenuItem.objects.filter(company=company, name__iexact=name).exclude(id=item_id).exists():
                    messages.error(request, f"A product with the name '{name}' already exists.")
                else:
                    try:
                        item = MenuItem.objects.get(id=item_id, company=company)
                        category = Category.objects.get(id=category_id, company=company)
                        item.name = name
                        item.price = price
                        item.category = category
                        if image:
                            item.image = image
                        item.save()
                        messages.success(request, "Product updated successfully.")
                    except Exception as e:
                        pass
        elif action == 'delete_item':
            item_id = request.POST.get('item_id')
            if item_id:
                try:
                    item = MenuItem.objects.get(id=item_id, company=company)
                    item.delete()
                    messages.success(request, "Product deleted successfully.")
                except Exception as e:
                    messages.error(request, "Error deleting product.")
        return HttpResponseRedirect(reverse('manage_menu'))
    categories = Category.objects.filter(company=company).prefetch_related('items')
    kot_printers = Printer.objects.filter(company=company, printer_type='kot', is_active=True)
    return render(request, 'core/manage_menu.html', {
        'categories': categories,
        'kot_printers': kot_printers,
        'company': company
    })

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate, TruncMonth
from datetime import datetime, timedelta
from .models import Order, OrderItem


@csrf_exempt
@login_required(login_url='login_view')
def create_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        company = request.user.profile.company
        
        items = data.get('items', [])
        payment_method = data.get('payment_method', 'cash')
        cash_amount = float(data.get('cash_amount', 0))
        upi_amount = float(data.get('upi_amount', 0))
        total = float(data.get('total', 0))
        
        table_id = data.get('table_id')
        action = data.get('action', 'checkout') # 'checkout' or 'kitchen'
        
        from .models import Table
        table = None
        if table_id:
            try:
                table = Table.objects.get(id=table_id, company=company)
            except Table.DoesNotExist:
                pass

        order_number_param = data.get('order_number')

        if order_number_param:
            # Append items directly to a specific existing order (used when cashier loads an order into the panel)
            try:
                order = Order.objects.get(order_number=order_number_param, company=company)
                order.total_amount = float(order.total_amount) + total
                order.status = 'pending'  # Re-open invoiced orders when items are added
                order.save()
            except Order.DoesNotExist:
                return JsonResponse({'error': 'Order not found'}, status=404)
        elif action == 'kitchen' and table:
            # Look for an active order (pending or invoiced)
            order = Order.objects.filter(company=company, table=table, status__in=['pending', 'invoiced']).first()
            if order:
                # Append to existing
                order.total_amount = float(order.total_amount) + total
                # If they add new items to an invoiced order, it becomes pending again
                order.status = 'pending'
                order.save()
            else:
                # Create new
                order = Order.objects.create(
                    company=company,
                    status='pending',
                    payment_method=payment_method,
                    cash_amount=cash_amount,
                    upi_amount=upi_amount,
                    total_amount=total,
                    billed_by=request.user,
                    table=table
                )
        else:
            status = 'paid' if action == 'checkout' else 'pending'
            order = Order.objects.create(
                company=company,
                status=status,
                payment_method=payment_method,
                cash_amount=cash_amount,
                upi_amount=upi_amount,
                total_amount=total,
                billed_by=request.user,
                table=table
            )

        new_order_items = []
        for item in items:
            menu_item = MenuItem.objects.get(id=item['id'])
            oi = OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                item_name=menu_item.name,
                quantity=item['qty'],
                price=menu_item.price,
                is_printed=False
            )
            new_order_items.append(oi)

        kot_results = {}
        bill_results = {}
        # Route KOT tickets directly to station network printers (KITCHEN, JUICE, etc.)
        kot_results = print_kot_for_order(order, new_order_items, synchronous=False)
        for oi in new_order_items:
            oi.is_printed = True
            oi.save()

        # If direct checkout, also send tax invoice to CASH printer
        if action == 'checkout':
            bill_results = print_bill_for_order(order, synchronous=False)

        return JsonResponse({
            'success': True,
            'order_number': order.order_number,
            'kot_results': kot_results,
            'bill_results': bill_results
        })
    return JsonResponse({'error': 'POST only'}, status=405)


@login_required(login_url='login_view')
def get_table_orders(request, table_id):
    if request.method == 'GET':
        company = request.user.profile.company
        orders = Order.objects.filter(company=company, table_id=table_id, status='pending')
        orders_data = []
        for o in orders:
            items_data = []
            for item in o.items.all():
                items_data.append({
                    'id': item.menu_item.id,
                    'name': item.item_name,
                    'qty': item.quantity,
                    'price': float(item.price),
                    'total': float(item.quantity * item.price)
                })
            orders_data.append({
                'order_number': o.order_number,
                'total_amount': float(o.total_amount),
                'created_at': o.created_at.strftime('%Y-%m-%d %I:%M %p'),
                'items': items_data
            })
        return JsonResponse({'success': True, 'orders': orders_data})
    return JsonResponse({'error': 'GET only'}, status=405)


@login_required(login_url='login_view')
def get_active_orders(request):
    if request.method == 'GET':
        company = request.user.profile.company
        orders = Order.objects.filter(company=company, status='pending').order_by('-created_at')
        orders_data = []
        for o in orders:
            items_data = []
            for item in o.items.all():
                items_data.append({
                    'id': item.menu_item.id,
                    'name': item.item_name,
                    'qty': item.quantity,
                    'price': float(item.price),
                    'total': float(item.quantity * item.price)
                })
            orders_data.append({
                'order_number': o.order_number,
                'total_amount': float(o.total_amount),
                'created_at': o.created_at.strftime('%Y-%m-%d %I:%M %p'),
                'items': items_data
            })
        return JsonResponse({'success': True, 'orders': orders_data})
    return JsonResponse({'error': 'GET only'}, status=405)


@csrf_exempt
@login_required(login_url='login_view')
def pay_order(request, order_number):
    if request.method == 'POST':
        data = json.loads(request.body)
        company = request.user.profile.company
        
        try:
            order = Order.objects.get(order_number=order_number, company=company)
            if order.status == 'paid':
                return JsonResponse({'error': 'Order is already paid', 'already_paid': True}, status=400)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
            
        order.payment_method = data.get('payment_method', 'cash')
        cash_val = float(data.get('cash_amount', 0))
        upi_val = float(data.get('upi_amount', 0))
        if cash_val == 0 and upi_val == 0:
            if order.payment_method == 'cash':
                cash_val = float(order.total_amount)
            elif order.payment_method == 'upi':
                upi_val = float(order.total_amount)
        order.cash_amount = cash_val
        order.upi_amount = upi_val
        order.status = 'paid'
        if not order.billed_by:
            order.billed_by = request.user
        order.save()
        
        bill_result = print_bill_for_order(order, synchronous=False)
        return JsonResponse({'success': True, 'order_number': order.order_number, 'bill_result': bill_result})
    return JsonResponse({'error': 'POST only'}, status=405)


@csrf_exempt
@login_required(login_url='login_view')
def transfer_table(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
            
        company = request.user.profile.company
        order_number = data.get('order_number')
        new_table_id = data.get('new_table_id')
        
        if not order_number or not new_table_id:
            return JsonResponse({'error': 'order_number and new_table_id are required'}, status=400)
            
        try:
            order = Order.objects.get(order_number=order_number, company=company)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
            
        if order.status == 'paid':
            return JsonResponse({'error': 'Cannot transfer an already paid order'}, status=400)
            
        try:
            new_table = Table.objects.get(id=new_table_id, company=company)
        except Table.DoesNotExist:
            return JsonResponse({'error': 'New table not found'}, status=404)
            
        old_table = order.table
        old_table_label = f"Table {old_table.table_number}" if old_table else "Direct Sale / No Table"
        new_table_label = f"Table {new_table.table_number}"
        
        if old_table and old_table.id == new_table.id:
            return JsonResponse({'error': 'Order is already assigned to this table'}, status=400)
            
        # Update order table
        order.table = new_table
        order.save()
        
        # Dispatch Table Transfer Notice to all Kitchen & Station Printers!
        kitchen_results = print_table_transfer_notice(order, old_table_label, new_table_label, synchronous=False)
        
        return JsonResponse({
            'success': True,
            'order_number': order.order_number,
            'old_table': old_table_label,
            'new_table': new_table_label,
            'new_table_id': new_table.id,
            'kitchen_results': kitchen_results
        })
    return JsonResponse({'error': 'POST only'}, status=405)


@login_required(login_url='login_view')
def order_history(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        return HttpResponseForbidden("Access Denied.")
    company = request.user.profile.company
    orders = Order.objects.filter(company=company).order_by('-created_at')

    search = request.GET.get('search', '').strip()
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    if search:
        orders = orders.filter(order_number__icontains=search)
    if date_from:
        orders = orders.filter(created_at__date__gte=date_from)
    if date_to:
        orders = orders.filter(created_at__date__lte=date_to)

    return render(request, 'core/order_history.html', {
        'orders': orders,
        'search': search,
        'date_from': date_from,
        'date_to': date_to,
        'total_results': orders.count(),
    })


@login_required(login_url='login_view')
def order_detail(request, order_number):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        return HttpResponseForbidden("Access Denied.")
    company = request.user.profile.company
    order = Order.objects.get(order_number=order_number, company=company)
    items = OrderItem.objects.filter(order=order)
    return render(request, 'core/order_detail.html', {'order': order, 'items': items})


@login_required(login_url='login_view')
def bill_view(request, order_number):
    company = request.user.profile.company
    order = Order.objects.get(order_number=order_number, company=company)
    items = OrderItem.objects.filter(order=order)
    return render(request, 'core/bill.html', {'order': order, 'items': items, 'company': company})


@login_required(login_url='login_view')
def sales_dashboard(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        return HttpResponseForbidden("Access Denied.")
    company = request.user.profile.company
    
    from django.utils import timezone
    today = timezone.localdate()
    month_start = today.replace(day=1)
    year_start = today.replace(month=1, day=1)

    all_orders = Order.objects.filter(company=company, status='paid')
    
    today_orders = all_orders.filter(created_at__date=today)
    month_orders = all_orders.filter(created_at__date__gte=month_start)
    year_orders = all_orders.filter(created_at__date__gte=year_start)

    today_total = today_orders.aggregate(total=Sum('total_amount'))['total'] or 0
    month_total = month_orders.aggregate(total=Sum('total_amount'))['total'] or 0
    year_total = year_orders.aggregate(total=Sum('total_amount'))['total'] or 0
    all_time_total = all_orders.aggregate(total=Sum('total_amount'))['total'] or 0

    today_cash = today_orders.aggregate(total=Sum('cash_amount'))['total'] or 0
    today_upi = today_orders.aggregate(total=Sum('upi_amount'))['total'] or 0
    month_cash = month_orders.aggregate(total=Sum('cash_amount'))['total'] or 0
    month_upi = month_orders.aggregate(total=Sum('upi_amount'))['total'] or 0

    today_count = today_orders.count()
    month_count = month_orders.count()

    # Product-wise sales - all time
    product_sales = OrderItem.objects.filter(
        order__company=company, order__status='paid'
    ).values('item_name').annotate(
        total_qty=Sum('quantity'),
        total_revenue=Sum('price')
    ).order_by('-total_revenue')

    # Product-wise sales - today
    product_today = OrderItem.objects.filter(
        order__company=company, order__status='paid',
        order__created_at__date=today
    ).values('item_name').annotate(
        total_qty=Sum('quantity'),
        total_revenue=Sum('price')
    ).order_by('-total_revenue')

    # Product-wise sales - this week
    week_start = today - timedelta(days=today.weekday())
    product_week = OrderItem.objects.filter(
        order__company=company, order__status='paid',
        order__created_at__date__gte=week_start
    ).values('item_name').annotate(
        total_qty=Sum('quantity'),
        total_revenue=Sum('price')
    ).order_by('-total_revenue')

    # Product-wise sales - this month
    product_month = OrderItem.objects.filter(
        order__company=company, order__status='paid',
        order__created_at__date__gte=month_start
    ).values('item_name').annotate(
        total_qty=Sum('quantity'),
        total_revenue=Sum('price')
    ).order_by('-total_revenue')

    # Daily sales for last 7 days
    daily_sales = all_orders.filter(
        created_at__date__gte=today - timedelta(days=6)
    ).annotate(
        day=TruncDate('created_at')
    ).values('day').annotate(
        total=Sum('total_amount'),
        count=Count('id')
    ).order_by('day')

    daily_labels = []
    daily_data = []
    for d in daily_sales:
        daily_labels.append(d['day'].strftime('%d %b'))
        daily_data.append(float(d['total']))

    # Expiry Warning
    expiry_warning = False
    days_left = None
    if company.valid_until:
        days_left = (company.valid_until - today).days
        if days_left <= 10:
            expiry_warning = True

    return render(request, 'core/sales_dashboard.html', {
        'expiry_warning': expiry_warning,
        'days_left': days_left,
        'today_total': today_total, 'month_total': month_total,
        'year_total': year_total, 'all_time_total': all_time_total,
        'today_cash': today_cash, 'today_upi': today_upi,
        'month_cash': month_cash, 'month_upi': month_upi,
        'today_count': today_count, 'month_count': month_count,
        'product_sales': product_sales,
        'product_today': product_today,
        'product_week': product_week,
        'product_month': product_month,
        'daily_labels': json.dumps(daily_labels),
        'daily_data': json.dumps(daily_data),
    })

from .report_service import generate_excel_report, generate_pdf_report
from django.http import HttpResponse

@login_required(login_url='login_view')
def export_sales_report(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        return HttpResponseForbidden("Access Denied: Store Admin only.")
    
    company = request.user.profile.company
    format_type = request.GET.get('format', 'excel').lower()
    period = request.GET.get('period', 'month').lower()
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    from django.utils import timezone
    from datetime import timedelta
    today = timezone.localdate()
    
    orders = Order.objects.filter(company=company)
    date_label = "All Time"
    
    if period == 'today':
        orders = orders.filter(created_at__date=today)
        date_label = f"Today ({today.strftime('%d %b %Y')})"
    elif period == 'week':
        week_start = today - timedelta(days=today.weekday())
        orders = orders.filter(created_at__date__gte=week_start)
        date_label = f"This Week ({week_start.strftime('%d %b')} - {today.strftime('%d %b %Y')})"
    elif period == 'month':
        month_start = today.replace(day=1)
        orders = orders.filter(created_at__date__gte=month_start)
        date_label = f"This Month ({month_start.strftime('%B %Y')})"
    elif period == 'year':
        year_start = today.replace(month=1, day=1)
        orders = orders.filter(created_at__date__gte=year_start)
        date_label = f"This Year ({today.year})"
    elif period == 'custom' or (date_from and date_to):
        if date_from:
            orders = orders.filter(created_at__date__gte=date_from)
        if date_to:
            orders = orders.filter(created_at__date__lte=date_to)
        date_label = f"{date_from or 'Start'} to {date_to or 'Present'}"
    
    orders = orders.order_by('-created_at')
    
    paid_orders = orders.filter(status='paid')
    total_sales = float(paid_orders.aggregate(total=Sum('total_amount'))['total'] or 0)
    total_cash = float(paid_orders.aggregate(total=Sum('cash_amount'))['total'] or 0)
    total_upi = float(paid_orders.aggregate(total=Sum('upi_amount'))['total'] or 0)
    total_orders_count = orders.count()
    avg_order_value = total_sales / total_orders_count if total_orders_count > 0 else 0
    
    summary_metrics = {
        'total_sales': total_sales,
        'total_orders': total_orders_count,
        'total_cash': total_cash,
        'total_upi': total_upi,
        'avg_order_value': avg_order_value
    }
    
    product_sales = OrderItem.objects.filter(
        order__in=paid_orders
    ).values('item_name').annotate(
        total_qty=Sum('quantity'),
        total_revenue=Sum('price')
    ).order_by('-total_revenue')
    
    timestamp_str = timezone.localtime().strftime('%Y%m%d_%H%M%S')
    company_slug = "".join([c if c.isalnum() else "_" for c in company.name])
    
    if format_type == 'pdf':
        pdf_buffer = generate_pdf_report(company, orders, product_sales, date_label, summary_metrics)
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{company_slug}_Report_{timestamp_str}.pdf"'
        return response
    else:
        excel_buffer = generate_excel_report(company, orders, product_sales, date_label, summary_metrics)
        response = HttpResponse(
            excel_buffer.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{company_slug}_Report_{timestamp_str}.xlsx"'
        return response

@login_required(login_url='login_view')
def super_admin_renew_company(request, company_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Access Denied.")
    if request.method == 'POST':
        company = Company.objects.get(id=company_id)
        valid_until = request.POST.get('valid_until')
        plan_name = request.POST.get('plan_name')
        
        if valid_until:
            company.valid_until = valid_until
        if plan_name:
            company.plan_name = plan_name
            
        company.save()
    return redirect('super_admin_dashboard')


@login_required(login_url='login_view')
def manage_tables(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        return HttpResponseForbidden("Access Denied: Only Store Admins can manage tables.")
    company = request.user.profile.company
    from .models import Table
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_table':
            table_number = request.POST.get('table_number')
            seating_capacity = request.POST.get('seating_capacity')
            if table_number and seating_capacity:
                if Table.objects.filter(company=company, table_number__iexact=table_number).exists():
                    messages.error(request, f"A table with number '{table_number}' already exists.")
                else:
                    Table.objects.create(table_number=table_number, seating_capacity=seating_capacity, company=company)
                    messages.success(request, "Table added successfully.")
        elif action == 'edit_table':
            table_id = request.POST.get('table_id')
            table_number = request.POST.get('table_number')
            seating_capacity = request.POST.get('seating_capacity')
            if table_id and table_number and seating_capacity:
                if Table.objects.filter(company=company, table_number__iexact=table_number).exclude(id=table_id).exists():
                    messages.error(request, f"A table with number '{table_number}' already exists.")
                else:
                    try:
                        table = Table.objects.get(id=table_id, company=company)
                        table.table_number = table_number
                        table.seating_capacity = seating_capacity
                        table.save()
                        messages.success(request, "Table updated successfully.")
                    except Exception as e:
                        pass
        elif action == 'delete_table':
            table_id = request.POST.get('table_id')
            if table_id:
                try:
                    table = Table.objects.get(id=table_id, company=company)
                    table.delete()
                    messages.success(request, "Table deleted successfully.")
                except Exception as e:
                    messages.error(request, "Error deleting table.")
        return HttpResponseRedirect(reverse('manage_tables'))
    tables = Table.objects.filter(company=company).order_by('table_number')
    return render(request, 'core/manage_tables.html', {'tables': tables})


@login_required(login_url='login_view')
def kot_view(request, order_number):
    company = request.user.profile.company
    order = Order.objects.get(order_number=order_number, company=company)
    items = OrderItem.objects.filter(order=order)
    
    new_only = request.GET.get('new_only') == '1'
    if new_only:
        items = items.filter(is_printed=False)
    
    category_filter = request.GET.get('category')
    if category_filter:
        items = items.filter(menu_item__category__name=category_filter)
    
    # Group items by category
    category_items = {}
    items_to_mark = []
    for item in items:
        cat_name = item.menu_item.category.name
        if cat_name not in category_items:
            category_items[cat_name] = []
        category_items[cat_name].append(item)
        items_to_mark.append(item.id)
        
    # Mark items as printed if this is a new KOT request
    if new_only and items_to_mark:
        OrderItem.objects.filter(id__in=items_to_mark).update(is_printed=True)
        
    return render(request, 'core/kot.html', {'order': order, 'category_items': category_items})

@csrf_exempt
@login_required(login_url='login_view')
def invoice_order(request, order_number):
    if request.method == 'POST':
        company = request.user.profile.company
        try:
            order = Order.objects.get(order_number=order_number, company=company, status='pending')
            order.status = 'invoiced'
            order.save()
            bill_result = print_bill_for_order(order, synchronous=False)
            return JsonResponse({'success': True, 'bill_result': bill_result})
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found or already invoiced'}, status=404)
    return JsonResponse({'error': 'POST only'}, status=405)


@csrf_exempt
@login_required(login_url='login_view')
def api_test_printer(request, printer_id):
    if request.method == 'POST':
        company = request.user.profile.company
        try:
            printer = Printer.objects.get(id=printer_id, company=company)
            success, msg = test_printer(printer, synchronous=True)
            return JsonResponse({'success': success, 'message': msg})
        except Printer.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Printer not found'}, status=404)
    return JsonResponse({'error': 'POST only'}, status=405)


@csrf_exempt
@login_required(login_url='login_view')
def api_print_kot(request, order_number):
    if request.method == 'POST':
        company = request.user.profile.company
        try:
            order = Order.objects.get(order_number=order_number, company=company)
            results = print_kot_for_order(order, synchronous=False)
            return JsonResponse({'success': True, 'results': results})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Order not found'}, status=404)
    return JsonResponse({'error': 'POST only'}, status=405)


@csrf_exempt
@login_required(login_url='login_view')
def api_print_bill(request, order_number):
    if request.method == 'POST':
        company = request.user.profile.company
        try:
            order = Order.objects.get(order_number=order_number, company=company)
            result = print_bill_for_order(order, synchronous=False)
            return JsonResponse({'success': True, 'result': result})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Order not found'}, status=404)
    return JsonResponse({'error': 'POST only'}, status=405)

