from django.db import models
from .product import Product  
from .customer import Customer 

class Order(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'Em Andamento'),
        ('completed', 'Finalizado'),
        ('open', 'Aberto'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) 
    products = models.ManyToManyField(Product)
    total_value = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')  

    def __str__(self):
        return f"Pedido {self.id} - {self.customer.name}"
