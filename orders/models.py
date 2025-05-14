from django.db import models
from goods.models import Products, Variation
from users.models import CustomUser

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В работе'),
        ('waiting_payment', 'Ожидает оплаты'),
        ('processing', 'Сборка'),
        ('shipped', 'Отправлен'),
        ('ended', 'Завершен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'Заказ #{self.pk} - {self.get_status_display()}'
    
    class Meta:
        verbose_name = "Заказы"
        verbose_name_plural = "Заказы"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} ({self.variation.size}) x {self.quantity}'
    
    class Meta:
        verbose_name = "Товар заказа"
        verbose_name_plural = "Товары заказов"
