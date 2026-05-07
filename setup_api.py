import os

settings_path = "restaurant_pos/settings.py"
with open(settings_path, 'r', encoding='utf-8') as f:
    settings = f.read()

if "'rest_framework'," not in settings:
    settings = settings.replace(
        "'core',",
        "'core',\n    'rest_framework',\n    'corsheaders',"
    )

if "'corsheaders.middleware.CorsMiddleware'," not in settings:
    settings = settings.replace(
        "'django.middleware.security.SecurityMiddleware',",
        "'django.middleware.security.SecurityMiddleware',\n    'corsheaders.middleware.CorsMiddleware',"
    )

if "CORS_ALLOW_ALL_ORIGINS = True" not in settings:
    settings += "\nCORS_ALLOW_ALL_ORIGINS = True\n"

with open(settings_path, 'w', encoding='utf-8') as f:
    f.write(settings)

serializers_code = """from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Company, UserProfile

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'is_active', 'pos_type']

class UserProfileSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'role', 'company', 'company_name']
"""
with open("core/serializers.py", "w", encoding='utf-8') as f:
    f.write(serializers_code)

api_views_code = """from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Company, UserProfile
from .serializers import CompanySerializer, UserProfileSerializer
from django.views.decorators.csrf import csrf_exempt

@api_view(['GET'])
def get_companies(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def manage_users_api(request):
    if request.method == 'GET':
        profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        company_id = data.get('company')
        
        if not username or not password:
            return Response({'error': 'Username and password required'}, status=400)
            
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=400)

        user = User.objects.create_user(username=username, password=password)
        company = Company.objects.filter(id=company_id).first() if company_id else None
        
        profile = UserProfile.objects.create(user=user, role=role, company=company)
        return Response({'success': True, 'message': 'User created successfully'})
"""
with open("core/api_views.py", "w", encoding='utf-8') as f:
    f.write(api_views_code)

urls_path = "core/urls.py"
with open(urls_path, 'r', encoding='utf-8') as f:
    urls = f.read()

if "api/" not in urls:
    urls = urls.replace(
        "from . import views",
        "from . import views\nfrom . import api_views"
    )
    urls = urls.replace(
        "]",
        "    path('api/companies/', api_views.get_companies, name='api_companies'),\n    path('api/users/', api_views.manage_users_api, name='api_users'),\n]"
    )
    with open(urls_path, 'w', encoding='utf-8') as f:
        f.write(urls)
