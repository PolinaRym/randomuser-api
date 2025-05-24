from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('user/<str:uuid>/', views.user_detail, name='user_detail'),
    path('random/', views.random_user, name='random_user'),
] 