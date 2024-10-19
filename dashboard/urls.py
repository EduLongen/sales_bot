from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Dashboard root
    path('add_category/', views.add_category, name='add_category'),
    path('add_message/', views.add_message, name='add_message'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_user/', views.add_user, name='add_user'),
    path('categories/', views.categories_list, name='categories'),
    path('clients/', views.clients_list, name='clients'),
    path('messages/', views.messages_list, name='messages'),
    path('orders/', views.orders_list, name='orders'),
    path('payment/', views.payment_page, name='payment'),
    path('products/', views.products, name='products'),
    path('transmission/', views.transmission, name='transmission'),
    path('users/', views.users_list, name='users'),
]
