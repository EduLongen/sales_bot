from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth import get_user_model
from .models import Client, Category, Product, Order
from .models import PixPayment

# Get the custom User model
User = get_user_model()

# Customize the User admin to include the custom role field
@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    fieldsets = DefaultUserAdmin.fieldsets + (  # Use default fieldsets and append 'role'
        ('Additional Info', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'role')
    search_fields = ('username', 'first_name', 'last_name', 'email')

@admin.register(PixPayment)
class PixPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'pix_key', 'qr_code_url', 'created_at')
    search_fields = ('pix_key', 'description')

# Register other models
admin.site.register(Client)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
