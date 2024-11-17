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
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    
class OrderSerializer(serializers.ModelSerializer):
    client_chat_id = serializers.IntegerField(write_only=True)
    items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'client_chat_id', 'status', 'total', 'created_at', 'updated_at', 'items']  # Inclua client_chat_id aqui

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        chat_id = validated_data.pop('client_chat_id')

        # Busca o cliente pelo chat_id
        client = Client.objects.get(chat_id=chat_id)
        validated_data['client'] = client

        # Cria o pedido
        order = Order.objects.create(**validated_data)

        # Calcula o total e cria os itens
        total = 0
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            price = product.price * quantity  # Calcula o preço total do item

            total += price
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )

        # Atualiza o total no pedido
        order.total = total
        order.save()

        return order

