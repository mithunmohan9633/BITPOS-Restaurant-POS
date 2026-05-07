# Fix 3: Update views to add product-level analytics (today, week, month)
path = 'core/views.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

old_product_sales = """    # Product-wise sales
    product_sales = OrderItem.objects.filter(
        order__company=company, order__status='paid'
    ).values('item_name').annotate(
        total_qty=Sum('quantity'),
        total_revenue=Sum('price')
    ).order_by('-total_revenue')"""

new_product_sales = """    # Product-wise sales - all time
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
    ).order_by('-total_revenue')"""

c = c.replace(old_product_sales, new_product_sales)

old_context = """        'product_sales': product_sales,"""
new_context = """        'product_sales': product_sales,
        'product_today': product_today,
        'product_week': product_week,
        'product_month': product_month,"""

c = c.replace(old_context, new_context)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
