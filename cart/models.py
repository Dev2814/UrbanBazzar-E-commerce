from django.db import models
from users.models import CustomUser 

class ShoppingSession(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Shopping Session for {self.user.email}"

class CartItem(models.Model):
    session = models.ForeignKey(ShoppingSession, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.product.price * self.quantity
    
