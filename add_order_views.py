# Step 2: Add order saving API and order views
views_path = 'core/views.py'
with open(views_path, 'r', encoding='utf-8') as f:
    views = f.read()

# Add new imports and views at the end
new_views = """
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
    
    search = request.GET.get('search', '')
    if search:
        orders = orders.filter(order_number__icontains=search)
    
    return render(request, 'core/order_history.html', {'orders': orders, 'search': search})


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
    today = timezone.now().date()
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

    # Product-wise sales
    product_sales = OrderItem.objects.filter(
        order__company=company, order__status='paid'
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

    return render(request, 'core/sales_dashboard.html', {
        'today_total': today_total, 'month_total': month_total,
        'year_total': year_total, 'all_time_total': all_time_total,
        'today_cash': today_cash, 'today_upi': today_upi,
        'month_cash': month_cash, 'month_upi': month_upi,
        'today_count': today_count, 'month_count': month_count,
        'product_sales': product_sales,
        'daily_labels': json.dumps(daily_labels),
        'daily_data': json.dumps(daily_data),
    })
"""

with open(views_path, 'a', encoding='utf-8') as f:
    f.write(new_views)

# Step 3: Update URLs
urls_code = """
from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path('', views.pos_dashboard, name='pos_dashboard'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('users/', views.manage_users, name='manage_users'),
    path('menu/', views.manage_menu, name='manage_menu'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/<str:order_number>/', views.order_detail, name='order_detail'),
    path('bill/<str:order_number>/', views.bill_view, name='bill_view'),
    path('sales/', views.sales_dashboard, name='sales_dashboard'),
    path('super-admin/', views.super_admin_dashboard, name='super_admin_dashboard'),
    path('super-admin/create-company/', views.super_admin_create_company, name='super_admin_create_company'),
    path('super-admin/create-admin/', views.super_admin_create_admin, name='super_admin_create_admin'),
    path('super-admin/toggle-company/<int:company_id>/', views.super_admin_toggle_company, name='super_admin_toggle_company'),
    path('api/create-order/', views.create_order, name='create_order'),
    path('api/companies/', api_views.get_companies, name='api_companies'),
    path('api/users/', api_views.manage_users_api, name='api_users'),
    path('api/menu/', api_views.get_menu, name='api_menu'),
]
"""
with open('core/urls.py', 'w', encoding='utf-8') as f:
    f.write(urls_code)
