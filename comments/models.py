from django.db import models
from products.models import Product
from accounts.models import User

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comment_product")
    commenting_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user1")
    approring_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user2", null=True, blank=True)
    comment_text = models.TextField()
    register_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    comment_parent = models.ForeignKey("Comment", on_delete=models.CASCADE, null=True, blank=True, related_name="comment_child")
    
    def __str__(self):
        return f"{self.product}- {self.commenting_user}"