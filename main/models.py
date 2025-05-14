from django.db import models

class SiteSettings(models.Model):
    background_image = models.ImageField(upload_to='backgrounds/', blank=True, null=True, verbose_name="Фоновое изображение")
    background_color = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Цвет фона (например, #00000080 для полупрозрачного)"
    )
    use_image = models.BooleanField(default=True, verbose_name="Использовать изображение как фон")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Настройки сайта"

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"
