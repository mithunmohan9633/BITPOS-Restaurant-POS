from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Company, UserProfile
from .serializers import CompanySerializer, UserProfileSerializer, CategorySerializer
from django.views.decorators.csrf import csrf_exempt

@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'success': False, 'error': 'Username and password required'}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                login(request, user)
            except Exception:
                pass

            role = 'superuser' if user.is_superuser else 'user'
            try:
                if user.profile:
                    role = user.profile.role
            except Exception:
                pass

            if user.is_superuser or role == 'admin':
                return Response({'success': False, 'error': 'Admin & Super Admin users must use the Web Dashboard. Mobile app is for Staff & Cashiers only.'}, status=400)

            return Response({
                'success': True,
                'username': user.username,
                'role': role
            })
        else:
            return Response({'success': False, 'error': 'Invalid username or password'}, status=400)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=500)

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

from .models import Category, Table

@api_view(['GET'])
def get_menu(request):
    categories = Category.objects.all().prefetch_related('items')
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_tables(request):
    company = request.user.profile.company if hasattr(request.user, 'profile') else None
    if not company:
        return Response({'success': False, 'error': 'Company not found'}, status=400)
    tables = Table.objects.filter(company=company)
    data = [{'id': t.id, 'table_number': t.table_number, 'seating_capacity': t.seating_capacity, 'is_occupied': t.is_occupied} for t in tables]
    return Response({'success': True, 'tables': data})
