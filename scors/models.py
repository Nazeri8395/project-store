from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from products.models import Product
from accounts.models import User

class Score(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="scores")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scores")
    register_date = models.DateTimeField(auto_now_add=True)
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.product.name} - {self.user.username} - {self.score}"
