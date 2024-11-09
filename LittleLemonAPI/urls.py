from django.urls import path, include

from . import views

urlpatterns = [
    path('menu-items', views.MenuItemView.as_view()),
    path('menu-items/<int:pk>', views.MenuDetailView.as_view()),
    path('categories', views.CategoryView.as_view()), 
    path('orders', views.OrderView.as_view()),
    path('orders/<int:pk>', views.OrderDetailView.as_view()),
    path('cart/menu-items', views.CartView.as_view()), 
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    # path('api/groups/manager/users', views.ManagerGroupUsersView.as_view(), ),
    # path('api/groups/manager/users/<int:user_id>', views.RemoveManagerUserView.as_view() ),
    # path('api/groups/delivery-crew/users',  views.DeliveryCrewUsersView.as_view()),
    # path('api/groups/delivery-crew/users/<int:user_id>',  views.RemoveDeliveryCrewUserView.as_view()),



]