from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('customer/add/', views.add_customer, name='add_customer'),
    path('customer/<int:pk>/', views.customer_detail, name='customer_detail'),
]
