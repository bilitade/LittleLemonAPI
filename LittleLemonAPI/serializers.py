from rest_framework import serializers
from .models import MenuItem, Category, Order, OrderItem, Cart
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']

class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    menuitem = MenuItemSerializer(read_only=True) 
    menuitem_id = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all(), source='menuitem', write_only=True)

    class Meta:
        model = Cart
        fields = ['user', 'user_id', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    delivery_crew = serializers.PrimaryKeyRelatedField(read_only=True)
    delivery_crew_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='delivery_crew', required=False, write_only=True)

    class Meta:
        model = Order
        fields = ['user', 'user_id', 'delivery_crew', 'delivery_crew_id', 'status', 'date', 'total']

class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), source='order', write_only=True)
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all(), source='menuitem', write_only=True)

    class Meta:
        model = OrderItem
        fields = ['order', 'order_id', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']
