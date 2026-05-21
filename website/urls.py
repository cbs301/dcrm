from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('student/add/', views.add_student, name='add_student'),
    path('student/<int:pk>/', views.student_detail, name='student_detail'),
    path('student/<int:pk>/edit/', views.edit_student, name='edit_student'),
    path('student/<int:pk>/delete/', views.delete_student, name='delete_student'),
]
