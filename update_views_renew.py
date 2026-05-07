path = 'core/views.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

new_view = """
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
"""

with open(path, 'a', encoding='utf-8') as f:
    f.write(new_view)
print("Updated views.py with renewal logic")
