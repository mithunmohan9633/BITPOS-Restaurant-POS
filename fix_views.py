path = 'core/views.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    "    return render(request, 'core/super_admin.html', {\n        'companies': companies,\n        'admins': admins,\n    })",
    "    active_count = companies.filter(is_active=True).count()\n    return render(request, 'core/super_admin.html', {\n        'companies': companies,\n        'admins': admins,\n        'active_count': active_count,\n    })"
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
