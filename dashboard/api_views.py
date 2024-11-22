from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework import filters
from .models import Product, Category, Client, Order, PixPayment
from .serializers import  OrderSerializer, ProductSerializer, CategorySerializer, ClientSerializer
from .models import Product
from .serializers import ProductSerializer
from rest_framework.exceptions import ValidationError
from django.db import transaction
from decimal import Decimal


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

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def all_clients(self, request):
        clients = Client.objects.filter(is_active=True)
        serializer = self.get_serializer(clients, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='chat/(?P<chat_id>[^/.]+)', permission_classes=[AllowAny])
    def get_by_chat_id(self, request, chat_id=None):
        try:
            # Tenta buscar o cliente pelo chat_id
            client = Client.objects.get(chat_id=chat_id)
            serializer = ClientSerializer(client)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Client.DoesNotExist:
            # Retorna um JSON vazio se não encontrar
            return Response({}, status=status.HTTP_200_OK)

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
    permission_classes = [AllowAny]

    def validate_client(self, chat_id):
        try:
            return Client.objects.get(chat_id=chat_id)
        except Client.DoesNotExist:
            raise ValidationError({
                "client_chat_id": "Cliente não encontrado com este chat_id."
            })

    def validate_total(self, order_items):
        """Valida e calcula o total do pedido baseado nos items"""
        if not order_items:
            raise ValidationError({"items": "O pedido deve conter pelo menos um item."})
        
        calculated_total = Decimal('0.00')
        for item in order_items:
            quantity = Decimal(str(item.get('quantity', 0)))
            price = Decimal(str(item.get('price', 0)))
            if quantity <= 0:
                raise ValidationError({"quantity": "A quantidade deve ser maior que zero."})
            if price <= 0:
                raise ValidationError({"price": "O preço deve ser maior que zero."})
            calculated_total += quantity * price
        
        return calculated_total

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            # Validar cliente
            chat_id = request.data.get('client_chat_id')
            client = self.validate_client(chat_id)

            # Validar e calcular total
            order_items = request.data.get('items', [])
            calculated_total = self.validate_total(order_items)

            # Criar pedido com transaction para garantir atomicidade
            serializer = self.get_serializer(data={
                **request.data,
                'total': calculated_total,
                'status': 'AwaitingPayment'
            })
            serializer.is_valid(raise_exception=True)
            order = serializer.save(client=client)

            # Criar o pagamento Pix
            pix_payment = PixPayment.objects.latest('created_at')

            return Response({
                "order_id": order.id,
                "qr_code_url": pix_payment.qr_code_url,
                "pix_key": pix_payment.pix_key,
                "description": pix_payment.description,
            }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            # Log the error for debugging
            import logging
            logging.error(f"Error creating order: {str(e)}")
            return Response({
                "detail": "Erro ao processar o pedido. Por favor, tente novamente."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
