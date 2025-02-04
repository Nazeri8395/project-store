from django.db import models

from accounts.models import User
from products.models import Product

class Favorite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="favorite_product")
    favorite_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite_user")
    register_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product} - {self.favorite_user}"