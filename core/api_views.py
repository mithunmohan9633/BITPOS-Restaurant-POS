from rest_framework.decorators import api_view
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

from .models import Category

@api_view(['GET'])
def get_menu(request):
    categories = Category.objects.all().prefetch_related('items')
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)
