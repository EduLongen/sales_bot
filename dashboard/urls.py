from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api_views  # Assuming you have api_views for API endpoints
from django.contrib.auth import views as auth_views

# Setting up the API router for REST API views
api_router = DefaultRouter()
api_router.register(r'users', api_views.UserViewSet)
api_router.register(r'clients', api_views.ClientViewSet)
api_router.register(r'categories', api_views.CategoryViewSet)
api_router.register(r'products', api_views.ProductViewSet)
api_router.register(r'orders', api_views.OrderViewSet)
api_router.register(r'order-items', api_views.OrderItemViewSet)
api_router.register(r'messages', api_views.MessageViewSet)
api_router.register(r'pix-payments', api_views.PixPaymentViewSet)
api_router.register(r'jwts', api_views.JWTViewSet)

urlpatterns = [
    # Template-based views
    path('', views.dashboard, name='dashboard'),  # Dashboard root
    path('register/', views.register, name='register'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_message/', views.add_message, name='add_message'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_user/', views.add_user, name='add_user'),
    path('categories/', views.categories_list, name='categories'),
    path('dashboard/categories/edit/<int:id>/', views.edit_category, name='edit_category'),
    path('dashboard/categories/delete/<int:id>/', views.delete_category, name='delete_category'),
    path('clients/', views.clients_list, name='clients'),
    path('messages/', views.messages_list, name='messages'),
    path('orders/', views.orders_list, name='orders'),
    path('payment/', views.payment_page, name='payment'),
    path('products/', views.products, name='products'),
    path('transmission/', views.transmission, name='transmission'),
    
    path('users/', views.users_list, name='users'),
    # Add other user-related views here
    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),  # Edit user URL
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),  # Delete user URL

    # Authentication routes
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # API routes
    path('api/', include(api_router.urls)),
]
