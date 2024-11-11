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
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['user', 'user_id', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']

    def validate(self, attrs):
        menuitem = attrs.get('menuitem')
        quantity = attrs.get('quantity', 1)

        if menuitem:
            unit_price = menuitem.price
            price = unit_price * quantity
            attrs['unit_price'] = unit_price
            attrs['price'] = price

        return attrs

class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), source='order', write_only=True)
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all(), source='menuitem', write_only=True)

    class Meta:
        model = OrderItem
        fields = ['order', 'order_id', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']

    def validate(self, attrs):
        quantity = attrs.get('quantity')
        menuitem = attrs.get('menuitem')
        
        if menuitem:
            unit_price = menuitem.price
            price = unit_price * quantity
            attrs['unit_price'] = unit_price
            attrs['price'] = price
        
        return attrs

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    delivery_crew = serializers.PrimaryKeyRelatedField(read_only=True)
    delivery_crew_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='delivery_crew', required=False, write_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'user_id', 'delivery_crew', 'delivery_crew_id', 'status', 'date', 'total', 'order_items']
