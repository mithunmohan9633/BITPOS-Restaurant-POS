path = 'core/urls.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

if 'renew-company' not in c:
    c = c.replace(
        "path('super-admin/toggle-company/<int:company_id>/', views.super_admin_toggle_company, name='super_admin_toggle_company'),",
        "path('super-admin/toggle-company/<int:company_id>/', views.super_admin_toggle_company, name='super_admin_toggle_company'),\n    path('super-admin/renew-company/<int:company_id>/', views.super_admin_renew_company, name='super_admin_renew_company'),"
    )

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("Updated urls.py")
