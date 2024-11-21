from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.files import File
from io import BytesIO
from django.utils.text import slugify
import qrcode

class User(AbstractUser):
    ROLE_CHOICES = [
        ('administrator', 'Administrator'),
        ('moderator', 'Moderator'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='moderator')
    is_active = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        Group,
        related_name="dashboard_user_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="dashboard_user_permissions",
        blank=True
    )

    def __str__(self):
        return self.username


class Client(models.Model):
    chat_id = models.BigIntegerField(null=False, unique=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=100, null=True)
    address = models.TextField(null=True)
    is_active = models.BooleanField(default=True, null=False)
    is_deleted = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    image_url = models.CharField(max_length=255, default='default_image_url.jpg')
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=255, blank=True, default="No description")  # Default value added
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Default added to avoid issues
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)  # Default removed, handle client manually
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Processing', 'Processing'),
            ('Shipped', 'Shipped'),
            ('Delivered', 'Delivered'),
            ('Cancelled', 'Cancelled')
        ],
        default='Pending'
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Default value for quantity
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Default value for price

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"


class Message(models.Model):
    name = models.TextField(max_length=255, blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    content = models.TextField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message at {self.created_at}"


class PixPayment(models.Model):
    pix_key = models.CharField(max_length=50)
    description = models.TextField(max_length=255, blank=True, null=True)
    qr_code_url = models.URLField(max_length=255, blank=True, null=True)
    qr_code_image = models.ImageField(upload_to='qr_codes', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pix Payment {self.id} - {self.pix_key}"

    def generate_qr_code(self):
        from .utils import generate_pix_qr_code
        
        # Generate QR Code Buffer
        qr_buffer = generate_pix_qr_code(self)
        
        # Save the QR Code Image
        self.qr_code_image.save(f'pix_qr_{slugify(self.description)}_{self.id}.png', File(qr_buffer), save=False)
        
        # Generate QR Code URL (Example: for API, dynamic hostname usage)
        self.qr_code_url = f'/media/{self.qr_code_image.name}'  # Assuming static MEDIA_PATH.
        
        # Save Model Changes
        self.save()


class JWT(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jwt_tokens')
    token = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"JWT for {self.user.username}"
