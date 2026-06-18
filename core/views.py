
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Company, Category, MenuItem, UserProfile


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
                # Check 1: Username must be unique
                if User.objects.filter(username=username).exists():
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
                try:
                    user = User.objects.get(id=user_id, profile__role='admin')
                    if User.objects.filter(username=username).exclude(id=user_id).exists():
                        messages.error(request, 'Username already taken.')
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
    categories = Category.objects.filter(company=company).prefetch_related('items')
    return render(request, 'core/pos_dashboard.html', {'categories': categories})


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
                if not User.objects.filter(username=username).exists():
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
def manage_menu(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        return HttpResponseForbidden("Access Denied: Only Store Admins can manage the menu.")
    company = request.user.profile.company
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_category':
            name = request.POST.get('name')
            if name:
                if Category.objects.filter(company=company, name__iexact=name).exists():
                    messages.error(request, f"A category with the name '{name}' already exists.")
                else:
                    Category.objects.create(name=name, company=company)
                    messages.success(request, "Category added successfully.")
        elif action == 'add_item':
            category_id = request.POST.get('category')
            name = request.POST.get('name')
            price = request.POST.get('price')
            if name and price and category_id:
                if MenuItem.objects.filter(company=company, name__iexact=name).exists():
                    messages.error(request, f"A product with the name '{name}' already exists.")
                else:
                    category = Category.objects.get(id=category_id, company=company)
                    MenuItem.objects.create(name=name, price=price, category=category, company=company)
                    messages.success(request, "Product added successfully.")
        elif action == 'edit_item':
            item_id = request.POST.get('item_id')
            category_id = request.POST.get('category')
            name = request.POST.get('name')
            price = request.POST.get('price')
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
                        item.save()
                        messages.success(request, "Product updated successfully.")
                    except Exception as e:
                        pass
        return HttpResponseRedirect(reverse('manage_menu'))
    categories = Category.objects.filter(company=company).prefetch_related('items')
    return render(request, 'core/manage_menu.html', {'categories': categories})

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

        order = Order.objects.create(
            company=company,
            status='paid',
            payment_method=payment_method,
            cash_amount=cash_amount,
            upi_amount=upi_amount,
            total_amount=total,
            billed_by=request.user,
        )

        for item in items:
            menu_item = MenuItem.objects.get(id=item['id'])
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                item_name=menu_item.name,
                quantity=item['qty'],
                price=menu_item.price,
            )

        return JsonResponse({'success': True, 'order_number': order.order_number})
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
