
from django.shortcuts import render
from rest_framework import generics, status,filters
from rest_framework.response import Response
from .models import Category, Order, MenuItem, OrderItem, Cart
from .serializers import MenuItemSerializer, CategorySerializer, OrderSerializer, CartSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get_permissions(self):
        """
        Allow GET requests without authentication (anonymous access).
        For POST, PUT, DELETE methods, authentication is required.
        """
        if self.request.method == 'GET':
            return []  # No permissions needed for GET (anonymous access)
        return [IsAuthenticated()]  # Apply IsAuthenticated for other methods


class MenuItemView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = {
        'category': ['exact'],
        'price': ['exact', 'gt', 'lt'],  
    }
    search_fields = ['title']
    ordering_fields = ['price', 'featured']

    def get_permissions(self):
        """
        Allow GET requests without authentication (anonymous access).
        For POST, PUT, DELETE methods, authentication is required.
        """
        if self.request.method == 'GET':
            return []  # No permissions needed for GET (anonymous access)
        return [IsAuthenticated()]  # Apply IsAuthenticated for other methods


    def post(self, request, *args, **kwargs):
        # Ensure only managers can create menu items
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return super().post(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # Ensure only managers can update menu items
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # Ensure only managers can delete menu items
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        # Allow all users to view menu items
        return super().get(request, *args, **kwargs)

class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['status'] 
    search_fields = ['id', 'user__username'] 
    ordering_fields = ['date', 'total'] 
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

 
    def get_queryset(self):
        """Filter orders based on the authenticated user."""
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Handle order creation, including cart processing and order item creation
        user = self.request.user
        cart_items = Cart.objects.filter(user=user)
        
        if not cart_items:
            return Response({'detail': 'No items in the cart to place an order.'}, status=status.HTTP_400_BAD_REQUEST)
        
        total_price = sum(item.price for item in cart_items)
        order = serializer.save(user=user, total=total_price)
        
        order_items = [OrderItem(
            order=order,
            menuitem=cart_item.menuitem,
            quantity=cart_item.quantity,
            unit_price=cart_item.unit_price,
            price=cart_item.price
        ) for cart_item in cart_items]

        OrderItem.objects.bulk_create(order_items)
        cart_items.delete()
        
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
 


class MenuDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


    def post(self, request, *args, **kwargs):
        # Ensure only managers can create menu items
        if not request.user.groups.filter(name="Manager").exists():
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return super().post(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # Ensure only managers can update menu items
        if not request.user.groups.filter(name="Manager").exists():
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        # Ensure only managers can partially update menu items
        if not request.user.groups.filter(name="Manager").exists():
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return super().patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # Ensure only managers can delete menu items
        if not request.user.groups.filter(name="Manager").exists():
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)

class CartView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


    def get_queryset(self):
        """Get all cart items for the authenticated user."""
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Add or update menu items in the user's cart."""
        user = self.request.user
        menuitem_id = self.request.data.get('menuitem_id')
        
        try:
            menuitem = MenuItem.objects.get(id=menuitem_id)
        except MenuItem.DoesNotExist:
            return Response({'detail': 'Menu item not found.'}, status=status.HTTP_404_NOT_FOUND)

        quantity = self.request.data.get('quantity', 1)
        
        try:
            quantity = int(quantity)
        except ValueError:
            return Response({'detail': 'Quantity must be a valid number.'}, status=status.HTTP_400_BAD_REQUEST)

        existing_cart_item = Cart.objects.filter(user=user, menuitem=menuitem).first()
        
        if existing_cart_item:
            existing_cart_item.quantity += quantity
            existing_cart_item.price = existing_cart_item.unit_price * existing_cart_item.quantity
            existing_cart_item.save()
            return Response(CartSerializer(existing_cart_item).data, status=status.HTTP_200_OK)

        cart_item = serializer.save(user=user, menuitem=menuitem, quantity=quantity)
        return Response(CartSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        """Delete all cart items for the authenticated user."""
        Cart.objects.filter(user=self.request.user).delete()
        return Response({'detail': 'All cart items deleted.'}, status=status.HTTP_204_NO_CONTENT)

 #APIView is used  beacuse its simple to do customization than genericView
class ManagerUserView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


    def get(self, request):
        """Returns all users in the 'Manager' group."""
        if not request.user.groups.filter(name="Manager").exists():
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        
        managers = User.objects.filter(groups__name="Manager")
        users_data = [{"id": user.id, "username": user.username} for user in managers]
        return Response(users_data)

    def post(self, request):
        """Assign a user to the 'Manager' group."""
        if not request.user.groups.filter(name="Manager").exists():
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            manager_group = Group.objects.get(name="Manager")
            user.groups.add(manager_group)
            return Response({'detail': 'User added to Manager group'}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({'detail': 'Manager group not found'}, status=status.HTTP_404_NOT_FOUND)


class ManagerUserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


    def delete(self, request, userId):
        """Remove a user from the 'Manager' group."""
        if not request.user.groups.filter(name="Manager").exists():
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            user = User.objects.get(id=userId)
            manager_group = Group.objects.get(name="Manager")
            user.groups.remove(manager_group)
            return Response({'detail': 'User removed from Manager group'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({'detail': 'Manager group not found'}, status=status.HTTP_404_NOT_FOUND)


class DeliveryCrewUserView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


    def get(self, request):
        """Returns all users in the 'Delivery crew' group."""
        if not request.user.groups.filter(name="Manager").exists():
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        # Debug: Print the list of users in the "Delivery crew" group
        delivery_crew = User.objects.filter(groups__name="Delivery crew")
        print("Delivery crew Users:", delivery_crew)  # This will print the QuerySet to the console
        users_data = [{"id": user.id, "username": user.username} for user in delivery_crew]
        return Response(users_data)


    def post(self, request):
        """Assign a user to the 'Delivery crew' group."""
        if not request.user.groups.filter(name="Manager").exists():
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            delivery_crew_group = Group.objects.get(name="Delivery crew")
            user.groups.add(delivery_crew_group)
            return Response({'detail': 'User added to Delivery crew group'}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({'detail': 'Delivery crew group not found'}, status=status.HTTP_404_NOT_FOUND)


class DeliveryCrewUserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


    def delete(self, request, userId):
        """Remove a user from the 'Delivery crew' group."""
        if not request.user.groups.filter(name="Manager").exists():
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            user = User.objects.get(id=userId)
            delivery_crew_group = Group.objects.get(name="Delivery crew")
            user.groups.remove(delivery_crew_group)
            return Response({'detail': 'User removed from Delivery crew group'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({'detail': 'Delivery crew group not found'}, status=status.HTTP_404_NOT_FOUND)

class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


    def post(self, request, *args, **kwargs):
        try:
            # Attempt to get the user's token
            token = Token.objects.get(user=request.user)
            token.delete()  # Delete the token
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            # If no token exists for the user, return an appropriate message
            return Response({"error": "Token not found. User may already be logged out."}, status=status.HTTP_400_BAD_REQUEST)