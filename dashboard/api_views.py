# In api_views.py
from rest_framework import viewsets
from .models import User, Client, Category, Product, Order, OrderItem, Message, PixPayment, JWT
from .serializers import (
    UserSerializer, ClientSerializer, CategorySerializer, ProductSerializer,
    OrderSerializer, OrderItemSerializer, MessageSerializer, PixPaymentSerializer, JWTSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class PixPaymentViewSet(viewsets.ModelViewSet):
    queryset = PixPayment.objects.all()
    serializer_class = PixPaymentSerializer

class JWTViewSet(viewsets.ModelViewSet):
    queryset = JWT.objects.all()
    serializer_class = JWTSerializer
