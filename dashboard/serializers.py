from rest_framework import serializers
from .models import User, Client, Category, Product, Order, OrderItem, Message, PixPayment, JWT


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_active', 'groups', 'user_permissions']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data.get('role', 'moderator'),
            is_active=validated_data.get('is_active', True)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'chat_id', 'name', 'phone_number', 'city', 'address', 'is_active']


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'subcategories']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)

    class Meta:
        model = Product
        fields = ['id', 'image_url', 'name', 'description', 'category', 'category_id', 'price']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_id', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), source='client', write_only=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'client', 'client_id', 'status', 'total', 'created_at', 'updated_at', 'items']


class MessageSerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)
    admin_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='administrator'), source='admin', write_only=True)

    class Meta:
        model = Message
        fields = ['id', 'admin', 'admin_id', 'content', 'created_at']


class PixPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PixPayment
        fields = ['id', 'pix_key', 'qr_code_url', 'created_at']


class JWTSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)

    class Meta:
        model = JWT
        fields = ['id', 'user', 'user_id', 'token', 'created_at']
