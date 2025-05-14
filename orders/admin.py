from django.contrib import admin
from .models import Order, OrderItem
from django.utils.safestring import mark_safe

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_image', 'variation_sku')
    fields = ('product_image', 'product', 'variation_sku', 'variation', 'quantity')

    def product_image(self, obj):
        try:
            image = obj.product.main_image.url  # или obj.product.images.all()[0].image.url
            return mark_safe(f'<img src="{image}" width="50" height="50" />')
        except:
            return '-'
    
    product_image.short_description = 'Фото'

    def variation_sku(self, obj):
        return obj.variation.sku if obj.variation else '-'
    
    variation_sku.short_description = 'Артикул вариации'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('user__phone_number', 'id')
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'variation_sku', 'variation', 'quantity', 'product_image')
    readonly_fields = ('product_image', 'variation_sku')

    def product_image(self, obj):
        try:
            image = obj.product.images.first()
            if image:
                return mark_safe(f'<img src="{image.image.url}" width="50" height="50" />')
            return '-'
        except:
            return '-'

    def variation_sku(self, obj):
        return obj.variation.sku if obj.variation else '-'