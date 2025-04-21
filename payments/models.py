from django.db import models

class PaymentDetails(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey('orders.OrderDetails', on_delete=models.CASCADE)  # FIXED
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.CharField(max_length=100)  # e.g., PayPal, Stripe, Razorpay
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # NEW
    created_at = models.DateTimeField(auto_now_add=True)  # NEW
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"Payment {self.id} - {self.provider}"


