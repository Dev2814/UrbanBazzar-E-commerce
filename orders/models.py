from django.db import models
from users.models import CustomUser
from store.models import Product
from payments.models import PaymentDetails

class OrderDetails(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    # Flattened address fields to support both primary & secondary
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.ForeignKey(PaymentDetails, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - User {self.user.email}"


class OrderItems(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(OrderDetails, on_delete=models.CASCADE, related_name='orderitems') 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Order {self.order.id} - {self.product.name} ({self.quantity})"
