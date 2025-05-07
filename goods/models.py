from ast import Tuple
from os import name
import re
from django.db import models
from django.templatetags.i18n import language
from django.urls import reverse


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
    
    name = models.CharField(max_length=150, unique=True, verbose_name="Название")
    sku = models.CharField(max_length=150, unique=True, verbose_name="Акртикул")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='url')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name='Скидка в %')
    is_available = models.BooleanField(default=True, verbose_name='Доступен')
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория', related_name='category')
    
    class Meta: 
        db_table = 'Product'
        verbose_name= 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ("id",) 

    def __str__(self):
        return self.name
    
    def get_all_variation(self):
        return self.variations.all()
    
    def get_first_photo(self):
        if self.images.first():
            return self.images.first().image.url
        else:
            return 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRy8iuEnCT2fJCI_Jm-gN9veRRHaCpkBbAWUw&s.jpg'
    
    def get_absolute_url(self):
        return reverse( 'catalog:product', kwargs={'product_slug':self.slug})
        
    def display_id(self):
        return f'{self.id:05}'
    
    def sell_price(self):
        if self.discount:
            return round(self.price - self.price*self.discount/100, 2)
        
        return self.price
    
# class VariationManager(models.Manager):
#     def colors(self):
#         return super(VariationManager, self).filter(variation_category='color', is_active=True)

#     def sizes(self):
#         return super(VariationManager, self).filter(variation_category='size', is_active=True)
    
# variation_category_choice = (
#     ('color', 'цвет'),
#     ('size', 'размер'),
# )    


# class Variation(models.Model):
#     product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Товар', related_name='variations')
#     sku = models.CharField(max_length=150, unique=True, verbose_name="Акртикул вариации")
#     (slug) = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='url')
#     variation_category = models.CharField(max_length=100, blank=True, null=True, choices=variation_category_choice, verbose_name='Категория '
#                                                                                                           'вариации')
#     variation_value = models.CharField(max_length=100, blank=True, null=True, verbose_name='Значение вариации')
#     is_active = models.BooleanField(default=True, verbose_name='Активно')
#     quantity = models.PositiveIntegerField(default=0, verbose_name='Колличество')
#     objects = VariationManager()        

#     def __str__(self):
#         return f' {self.variation_category} : {self.variation_value}  - {self.quantity} шт.'

#     class Meta:
#         verbose_name = 'Вариацию'
#         verbose_name_plural = 'Вариации'    
        
class Variation(models.Model):
    product = models.ForeignKey('Products', on_delete=models.CASCADE, related_name='variations')
    sku = models.CharField(max_length=150, unique=True, verbose_name="Акртикул вариации")
    size = models.CharField(max_length=20, choices=[('116-122', '116-122'), ('122-128', '122-128'), ('128-134', '128-134'), ('134-140', '134-140'), ('140-146', '140-146'), ('146-152', '146-152'), ('152-158', '152-158'), ('158-164', '158-164'), ('164-170', '164-170'), ('170-176', '170-176'), ('176-182', '176-182')], blank=True, null=True)
    producer_size = models.CharField(max_length=20, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.size} - {self.producer_size}'
    
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