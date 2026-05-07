path = 'core/views.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Update super_admin_dashboard to include global revenue
old_sa_dashboard = """@login_required(login_url='login_view')
def super_admin_dashboard(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Access Denied.")
    companies = Company.objects.all().order_by('-created_at')
    admins = UserProfile.objects.filter(role='admin').select_related('user', 'company')
    active_count = Company.objects.filter(is_active=True).count()
    return render(request, 'core/super_admin.html', {
        'companies': companies, 
        'admins': admins, 
        'active_count': active_count
    })"""

new_sa_dashboard = """@login_required(login_url='login_view')
def super_admin_dashboard(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Access Denied.")
    companies = Company.objects.all().order_by('-created_at')
    admins = UserProfile.objects.filter(role='admin').select_related('user', 'company')
    active_count = Company.objects.filter(is_active=True).count()
    
    # Global Revenue
    global_revenue = Order.objects.filter(status='paid').aggregate(total=Sum('total_amount'))['total'] or 0
    
    return render(request, 'core/super_admin.html', {
        'companies': companies, 
        'admins': admins, 
        'active_count': active_count,
        'global_revenue': global_revenue
    })"""

c = c.replace(old_sa_dashboard, new_sa_dashboard)

# Update super_admin_create_company to handle valid_until and plan_name
old_sa_create = """@login_required(login_url='login_view')
def super_admin_create_company(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Access Denied.")
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        pos_type = request.POST.get('pos_type')
        Company.objects.create(name=name, address=address, pos_type=pos_type)
        return redirect('super_admin_dashboard')"""

new_sa_create = """@login_required(login_url='login_view')
def super_admin_create_company(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Access Denied.")
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        pos_type = request.POST.get('pos_type')
        plan_name = request.POST.get('plan_name', 'Standard')
        valid_until = request.POST.get('valid_until')
        
        Company.objects.create(
            name=name, 
            address=address, 
            pos_type=pos_type,
            plan_name=plan_name,
            valid_until=valid_until if valid_until else None
        )
        return redirect('super_admin_dashboard')"""

c = c.replace(old_sa_create, new_sa_create)

# Update sales_dashboard to include expiry warning
old_sales_view = """    return render(request, 'core/sales_dashboard.html', {"""
new_sales_view = """    # Expiry Warning
    expiry_warning = False
    days_left = None
    if company.valid_until:
        days_left = (company.valid_until - today).days
        if days_left <= 10:
            expiry_warning = True

    return render(request, 'core/sales_dashboard.html', {
        'expiry_warning': expiry_warning,
        'days_left': days_left,"""

c = c.replace(old_sales_view, new_sales_view)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("Updated views.py")
