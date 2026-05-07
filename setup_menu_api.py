import os

serializers_path = "core/serializers.py"
with open(serializers_path, 'r', encoding='utf-8') as f:
    serializers_content = f.read()

if "MenuItemSerializer" not in serializers_content:
    new_serializers = """
from .models import Category, MenuItem

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price']

class CategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'items']
"""
    with open(serializers_path, 'a', encoding='utf-8') as f:
        f.write(new_serializers)


api_views_path = "core/api_views.py"
with open(api_views_path, 'r', encoding='utf-8') as f:
    api_views_content = f.read()

if "get_menu" not in api_views_content:
    api_views_content = api_views_content.replace(
        "from .serializers import CompanySerializer, UserProfileSerializer",
        "from .serializers import CompanySerializer, UserProfileSerializer, CategorySerializer"
    )
    new_api_view = """
from .models import Category

@api_view(['GET'])
def get_menu(request):
    categories = Category.objects.all().prefetch_related('items')
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)
"""
    with open(api_views_path, 'a', encoding='utf-8') as f:
        f.write(new_api_view)


urls_path = "core/urls.py"
with open(urls_path, 'r', encoding='utf-8') as f:
    urls_content = f.read()

if "api_menu" not in urls_content:
    urls_content = urls_content.replace(
        "]",
        "    path('api/menu/', api_views.get_menu, name='api_menu'),\n]"
    )
    with open(urls_path, 'w', encoding='utf-8') as f:
        f.write(urls_content)

