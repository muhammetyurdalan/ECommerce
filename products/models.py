from django.db import models
from django.db.models import Sum


class Category(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
  
  
class Product(models.Model):
    category = models.ForeignKey(Category, 
        on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    score = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    is_done = models.BooleanField(default=False)   
    
    def __str__(self):
        return self.name
    
    def update_stock(self):
        result = self.variations.aggregate(total=Sum('stock'))
        self.stock = result['total'] or 0
        self.save(update_fields=['stock'])

    
class Variation(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class VariationOption(models.Model):
    variation = models.ForeignKey(Variation, 
        on_delete=models.CASCADE, related_name="options")
    value = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.variation.name}: {self.value}"


class ProductVariation(models.Model):
    product = models.ForeignKey(Product, 
        on_delete=models.CASCADE, related_name="variations")
    variation_option = models.ForeignKey(VariationOption, 
        on_delete=models.CASCADE, related_name="variations")
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.variation_option}"
    
    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)
        self.product.update_stock()


class OrderStatus(models.TextChoices):
    PENDING = 'PENDING'
    PROCESSING = 'PROCESSING'
    SHIPPING = 'SHIPPING'
    DELIVERED = 'DELIVERED'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
    RETURNED = 'RETURNED'
    REFUNDED = 'REFUNDED'
    FAILED = 'FAILED'

class Order(models.Model):
    user = models.ForeignKey('users.User', 
        on_delete=models.CASCADE, related_name="orders")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, 
        blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, 
        choices=OrderStatus.choices, default='PENDING')
    address = models.CharField(max_length=255)
    city = models.ForeignKey('users.City', 
        on_delete=models.PROTECT, related_name="orders")
    payment_id = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, 
        on_delete=models.CASCADE, related_name="items")
    product_variation = models.ForeignKey(ProductVariation, 
        on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"OrderItem {self.id} for Order {self.order.id}"


    