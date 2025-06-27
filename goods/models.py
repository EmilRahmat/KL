from ast import Tuple
from os import name
import re
from django.db import models
from django.templatetags.i18n import language
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

class Categories(models.Model):
    objects = models.Manager()
    
    name = models.CharField(max_length=150, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='url')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Категория', related_name= 'subcategory')
    
    class Meta:
        db_table = 'Categorie'
        verbose_name= 'Категорию'
        verbose_name_plural = 'Категории'
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse( 'catalog:index', kwargs={'category_slug':self.slug})
        
class Products(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=150, unique=False, verbose_name="Название")
    sku = models.CharField(max_length=150, unique=True, verbose_name="Артикул")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='url')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    season = models.CharField(
        max_length=20,
        choices=[
            ('spring_summer', 'Весна-Лето'),
            ('autumn_winter', 'Осень-Зима'),
            ('all_season', 'На любой сезон'),
        ],
        default='all_season',
        verbose_name='Сезонность'
    )
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name='Скидка в %')
    created_at = models.DateTimeField(default=timezone.now)
    is_available = models.BooleanField(default=True, verbose_name='Доступен')
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория', related_name='category')

    class Meta:
        db_table = 'Product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ("id",)

    def update_availability(self):
        has_stock = self.variations.filter(quantity__gt=0, is_active=True).exists()
        self.is_available = has_stock
        self.save(update_fields=["is_available"])
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk and not self.slug and self.sku:
            self.slug = str(self.sku)
        super().save(*args, **kwargs)

    def get_colors_display(self):
        from django.db.models import F

        colors = self.variations \
            .filter(color__isnull=False) \
            .values_list('color', flat=True) \
            .distinct()

        # Преобразуем slug цвета в человекочитаемый (из choices)
        color_choices = dict(Variation._meta.get_field('color').choices)
        return ', '.join([color_choices.get(color, color) for color in colors if color])
    
    def get_all_variation(self):
        return self.variations.all()

    def get_first_photo(self):
        if self.images.first():
            return self.images.first().image.url
        else:
            return 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRy8iuEnCT2fJCI_Jm-gN9veRRHaCpkBbAWUw&s.jpg'

    def get_absolute_url(self):
        return reverse('catalog:product', kwargs={'product_slug': self.slug})

    def display_id(self):
        return f'{self.id:05}'

    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        return self.price
    
     

    
 
class Variation(models.Model):
    product = models.ForeignKey('Products', on_delete=models.CASCADE, related_name='variations')
    sku = models.CharField(max_length=150, unique=True, verbose_name="Акртикул вариации")
    size = models.CharField(max_length=20, choices=[('116-122', '116-122'), ('122-128', '122-128'), ('128-134', '128-134'), ('134-140', '134-140'), ('140-146', '140-146'), ('146-152', '146-152'), ('152-158', '152-158'), ('158-164', '158-164'), ('164-170', '164-170'), ('170-176', '170-176'), ('176-182', '176-182'), ('146-164', '146-164'), ('158-176', '158-170'), ('30 обувь', '30 обувь'), ('31 обувь', '31 обувь'), ('32 обувь', '32 обувь'), ('33 обувь', '33 обувь'), ('34 обувь', '34 обувь'), ('35 обувь', '35 обувь'), ('36 обувь', '36 обувь'), ('37 обувь', '37 обувь'), ('38 обувь', '38 обувь'), ('39 обувь', '39 обувь'), ('40 обувь', '40 обувь'),], blank=True, null=True)
    color = models.CharField(max_length=20, choices=[('black', 'черный'), ('white', 'белый'), ('red', 'красный'), ('beige', 'бежевый'), ('khaki', 'хаки'), ('ping', 'розовый'), ('viol', 'фиолетовый'), ('blue', 'синий'), ('green', 'зеленый'), ('yellow', 'желтый'), ('grey', 'серый'), ('brown', 'коричневый'), ('burgundy', 'бордовый'), ], blank=True, null=True)
    producer_size = models.CharField(max_length=20, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.size} - {self.producer_size}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_availability()
    
    class Meta:
        verbose_name = 'Вариация'
        verbose_name_plural = 'Вариации'

class Gallery(models.Model):
    image = models.ImageField(upload_to='good_images', verbose_name='Изображения вариаций')
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, related_name='images')
    
    def __str__(self):
        return self.product.name
    
    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Фотогалерея товаров'


class ProcessedReceipt(models.Model):
    receipt_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.receipt_id