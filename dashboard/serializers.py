from rest_framework import serializers
from .models import User, Client, Category, Product, Message, PixPayment, JWT, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    products = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'is_active', 'products']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)

    class Meta:
        model = Product
        fields = ['id', 'image_url', 'name', 'description', 'category', 'category_id', 'price']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'chat_id', 'name', 'phone_number', 'city', 'address', 'is_active']


class MessageSerializer(serializers.ModelSerializer):
    admin = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='administrator'), source='admin', write_only=True)

    class Meta:
        model = Message
        fields = ['id', 'admin', 'name', 'description', 'text', 'created_at']


class PixPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PixPayment
        fields = ['id', 'pix_key', 'description', 'qr_code_url', 'created_at']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # Detalhes do produto

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    client = ClientSerializer()  # Detalhes do cliente
    items = OrderItemSerializer(many=True)  # Lista de itens do pedido

    class Meta:
        model = Order
        fields = ['id', 'client', 'status', 'total', 'created_at', 'updated_at', 'items']

    # Sobrescrevendo o método para salvar os itens do pedido
    def create(self, validated_data):
        items_data = validated_data.pop('items')  # Remove items
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    # Sobrescrevendo o método para atualizar os itens do pedido
    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        instance = super().update(instance, validated_data)

        if items_data:
            # Remove itens antigos
            instance.items.all().delete()
            # Cria os novos itens
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)

        return instance