from django.shortcuts import render
from rest_framework import generics
from .models import Category, Order, MenuItem, OrderItem, Cart
from .serializers import MenuItemSerializer

class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
