from django.db import models
from .category import Category 

class Product(models.Model):
    image = models.ImageField(upload_to='product_images/') 
    name = models.CharField(max_length=255)
    description = models.TextField()  
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name