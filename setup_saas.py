import os

# 1. Update Models
path_models = 'core/models.py'
with open(path_models, 'r', encoding='utf-8') as f:
    content = f.read()

company_replacement = """class Company(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    POS_CHOICES = (('restaurant', 'Restaurant'), ('retail', 'Retail'))
    pos_type = models.CharField(max_length=20, choices=POS_CHOICES, default='restaurant')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name"""

if "class Company(models.Model):" in content:
    start_idx = content.find("class Company(models.Model):")
    end_idx = content.find("class Category(models.Model):")
    content = content[:start_idx] + company_replacement + "\n\n" + content[end_idx:]

with open(path_models, 'w', encoding='utf-8') as f:
    f.write(content)

# 2. Create Middleware
middleware_code = """from django.shortcuts import redirect
from django.contrib.auth import logout

class SubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_superuser:
            if hasattr(request.user, 'profile') and request.user.profile.company:
                if not request.user.profile.company.is_active:
                    logout(request)
                    return redirect('/login/?error=subscription')
        
        return self.get_response(request)
"""
with open('core/middleware.py', 'w', encoding='utf-8') as f:
    f.write(middleware_code)

# 3. Add Middleware to Settings
path_settings = 'restaurant_pos/settings.py'
with open(path_settings, 'r', encoding='utf-8') as f:
    settings = f.read()

if "'core.middleware.SubscriptionMiddleware'," not in settings:
    settings = settings.replace(
        "'django.contrib.messages.middleware.MessageMiddleware',", 
        "'django.contrib.messages.middleware.MessageMiddleware',\n    'core.middleware.SubscriptionMiddleware',"
    )
with open(path_settings, 'w', encoding='utf-8') as f:
    f.write(settings)

# 4. Update login.html to show subscription error from URL parameter
path_login = 'core/templates/core/login.html'
with open(path_login, 'r', encoding='utf-8') as f:
    login_html = f.read()

error_check = """        {% if request.GET.error == 'subscription' %}
            <div class='error' style='color:#C96459;font-weight:800;padding:10px;background:#FFF9F8;border:2px solid #C96459;border-radius:8px;margin-bottom:15px'>Your subscription has expired or is deactivated. Please contact support.</div>
        {% endif %}
        {% if error %}<div class='error'>{{ error }}</div>{% endif %}"""

if "{% if request.GET.error" not in login_html:
    login_html = login_html.replace("{% if error %}<div class='error'>{{ error }}</div>{% endif %}", error_check)
with open(path_login, 'w', encoding='utf-8') as f:
    f.write(login_html)
