from django.shortcuts import render
from rest_framework import generics
from .models import Category, Order, MenuItem, OrderItem, Cart
from .serializers import MenuItemSerializer, CategorySerializer, OrderSerializer, CartSerializer

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()  
    serializer_class = OrderSerializer 

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()  
    serializer_class = OrderSerializer 


class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class MenuDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


