from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import filters
from .models import Product, Category, Client, Order, PixPayment
from .serializers import  OrderSerializer, ProductSerializer, CategorySerializer, ClientSerializer
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from rest_framework.decorators import api_view


class BlockAllAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        return False

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def all_categories(self, request):
        categories = Category.objects.filter(is_active=True)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)


class ProductByCategoryView(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ['name', 'price']
    ordering = ['name']

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Product.objects.filter(category_id=category_id, is_active=True)



class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Product.objects.filter(is_active=True)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(is_active=True)
    
class ClientCreateView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [AllowAny]
    
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @action(detail=False, methods=['get'], url_path='last-order/(?P<chat_id>[^/.]+)', permission_classes=[AllowAny])
    def last_order(self, request, chat_id=None):
        # Busca o cliente pelo chat_id
        client = get_object_or_404(Client, chat_id=chat_id)

        # Busca o último pedido do cliente
        last_order = Order.objects.filter(client=client).order_by('-created_at').first()

        if last_order:
            order_serializer = OrderSerializer(last_order)
            return Response(order_serializer.data)
        else:
            return Response({'message': 'No orders found for this client'}, status=status.HTTP_404_NOT_FOUND)


from rest_framework.exceptions import NotFound

class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        chat_id = self.request.data.get('client_chat_id')
        client = Client.objects.get(chat_id=chat_id)
        serializer.save(client=client)  # Salva o pedido associado ao cliente

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        try:
            # Busca o último PixPayment criado
            pix_payment = PixPayment.objects.latest('created_at')
            
            # Retorna o QR Code relacionado
            return Response({
                "qr_code_url": pix_payment.qr_code_url,
                "qr_code_image": pix_payment.qr_code_image.url if pix_payment.qr_code_image else None,
                "description": pix_payment.description,
            }, status=status.HTTP_201_CREATED)
        
        except PixPayment.DoesNotExist:
            # Retorna uma resposta apropriada se não houver PixPayment
            raise NotFound(detail="Nenhum PixPayment foi encontrado.", code=404)
