path = 'core/views.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Update login routing - Admin goes to sales dashboard, User goes to POS
old_login_routing = """            if user.is_superuser:
                return HttpResponseRedirect(reverse('super_admin_dashboard'))
            elif hasattr(user, 'profile') and user.profile.role == 'admin':
                return HttpResponseRedirect(reverse('pos_dashboard'))
            else:
                return HttpResponseRedirect(reverse('pos_dashboard'))"""

new_login_routing = """            if user.is_superuser:
                return HttpResponseRedirect(reverse('super_admin_dashboard'))
            elif hasattr(user, 'profile') and user.profile.role == 'admin':
                return HttpResponseRedirect(reverse('sales_dashboard'))
            else:
                return HttpResponseRedirect(reverse('pos_dashboard'))"""

c = c.replace(old_login_routing, new_login_routing)

# Update POS dashboard - block admin access, only users can sell
old_pos = """@login_required(login_url='login_view')
def pos_dashboard(request):
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('super_admin_dashboard'))
    if not hasattr(request.user, 'profile') or not request.user.profile.company:
        return HttpResponseForbidden("Your account is not assigned to any store.")
    company = request.user.profile.company
    categories = Category.objects.filter(company=company).prefetch_related('items')
    return render(request, 'core/pos_dashboard.html', {'categories': categories})"""

new_pos = """@login_required(login_url='login_view')
def pos_dashboard(request):
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('super_admin_dashboard'))
    if not hasattr(request.user, 'profile') or not request.user.profile.company:
        return HttpResponseForbidden("Your account is not assigned to any store.")
    if request.user.profile.role == 'admin':
        return HttpResponseRedirect(reverse('sales_dashboard'))
    company = request.user.profile.company
    categories = Category.objects.filter(company=company).prefetch_related('items')
    return render(request, 'core/pos_dashboard.html', {'categories': categories})"""

c = c.replace(old_pos, new_pos)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
