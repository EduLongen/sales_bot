from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import filters
from .models import Product, Category, Client, Order
from .serializers import OrderSerializer, ProductSerializer, CategorySerializer, ClientSerializer
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
    permission_classes = [BlockAllAccess]

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def all_categories(self, request):
        categories = Category.objects.filter(is_active=True)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)


class ProductByCategoryView(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ['name', 'price']  # Permite ordenar por nome ou preço
    ordering = ['name']  # Ordenar por nome por padrão

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Product.objects.filter(category_id=category_id)



class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class ClientCreateView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def last_order(self, request, pk=None):
        client = get_object_or_404(Client, pk=pk)

        last_order = Order.objects.filter(client=client).order_by('-created_at').first()

        if last_order:
            order_serializer = OrderSerializer(last_order)
            return Response(order_serializer.data)
        else:
            return Response({'message': 'No orders found for this client'}, status=status.HTTP_404_NOT_FOUND)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


@api_view(['POST'])
def create_order(request):
    if request.method == 'POST':
        # O serializer vai processar os dados do pedido e seus itens
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            # Salva o pedido e os itens associados
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)