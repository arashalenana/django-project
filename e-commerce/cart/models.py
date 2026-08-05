from django.db import models
from django.conf import settings
from products.models import Product
# Create your models here.
class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_cart_item_per_user_product')
        ]

    def __str__(self):
        return f'{self.quantity} x {self.product.name} ({self.user.username})'

    @property
    def subtotal(self):
        return self.product.display_price * self.quantity