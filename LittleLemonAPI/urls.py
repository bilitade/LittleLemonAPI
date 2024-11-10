from django.urls import path, include

from . import views

urlpatterns = [
    path('menu-items', views.MenuItemView.as_view()),
    path('menu-items/<int:pk>', views.MenuDetailView.as_view()),
    path('categories', views.CategoryView.as_view()), 
    path('orders', views.OrderView.as_view()),
    path('orders/<int:pk>', views.OrderDetailView.as_view()),

    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('cart/menu-items', views.CartView.as_view()),
   path('groups/manager/users', views.ManagerUserView.as_view(), name='manager_user_list'),
    path('groups/manager/users/<int:userId>', views.ManagerUserDetailView.as_view(), name='manager_user_detail'),
    path('groups/delivery-crew/users', views.DeliveryCrewUserView.as_view(), name='delivery_crew_user_list'),
    path('groups/delivery-crew/users/<int:userId>', views.DeliveryCrewUserDetailView.as_view(), name='delivery_crew_user_detail'),
]



