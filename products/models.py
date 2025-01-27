from django.db import models
from django.utils import timezone
from products.utils import FileUpload

class Brand(models.Model):
    brand_title = models.CharField( max_length=100)
    file_upload = FileUpload('images','brans')
    image_name = models.ImageField(upload_to=file_upload.upload_to) 
    
    def __str__(self):
        return  self.brand_title
    
class ProductGroup(models.Model):
    group_title = models.CharField(max_length=100)
    file_upload = FileUpload('images','product_group')
    image_name = models.ImageField(upload_to=file_upload.upload_to)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    register_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(default=timezone.now)
    group_parent = models.ForeignKey("ProductGroup", on_delete=models.CASCADE, blank=True, null=True, related_name="groups")
    
    def __str__(self):
        return self.group_title
    
class Feature(models.Model):
    feature_name =  models.CharField(max_length=100)
    product_group = models.ManyToManyField(ProductGroup, related_name="feature_of_group")
    
    def __str__(self):
        return self.feature_name
    
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    file_upload = FileUpload('images','products')
    image_name = models.ImageField(upload_to=file_upload.upload_to)
    price = models.PositiveBigIntegerField(default=0)
    product_group = models.ManyToManyField(ProductGroup, related_name="product_of_groups")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,null=True, related_name='brands_of_groups')
    is_active = models.BooleanField(default=True)
    register_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.product_name

class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.product}-{self.feature}-{self.value}"
class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file_upload = FileUpload('images','products')
    image_name = models.ImageField(upload_to=file_upload.upload_to)
    