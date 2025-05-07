from django.contrib import admin
from django.utils.html import format_html
from goods.models import Categories,Products,Variation,Gallery
from django.utils.safestring import mark_safe
from django.urls import path
from django.http import HttpResponseRedirect
from django.contrib import messages
from .utils import update_stock_from_excel  # Импортируем функцию



class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery
    extra = 1
    
class VariationInline(admin.TabularInline):
    fk_name = 'product'
    model = Variation
    extra = 1   
    
class ProductsInline(admin.TabularInline):
    fk_name = 'category'
    model = Products
    extra = 1


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug', 'parent')
    inlines = (ProductsInline,)
    
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'sku', 'price', 'get_variation_count', 'discount', 'get_photo', 'is_available')
    list_editable = ('price', 'discount', 'is_available')
    prepopulated_fields = {'slug':('name',)}
    list_filter = ('name', 'price')
    list_display_links = ('name',)
    inlines = (GalleryInline, VariationInline)
    
    def get_variation_count(self, object):
        if object.variations:
            return str(len(object.variations.all()))
        else:
            return '0'
    
    get_variation_count.short_description = 'Общее колличество'
    
    def get_photo(self, object):
        if object.images.all():
            return mark_safe(f'<img src="{object.images.all()[0].image.url}" width="50">')
        else:
            return '-'
        
    
@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'sku', 'size','producer_size', 'quantity', 'is_active')
    list_editable = ('is_active', 'quantity', 'size')
    list_filter = ('product', 'size', 'producer_size')
    search_fields = ('product__product_name',)
    prepopulated_fields = {'sku':('sku',)}
    change_list_template = "admin/variation_changelist.html"  # Кастомный шаблон

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('update-stock/', self.admin_site.admin_view(self.update_stock))
        ]
        return custom_urls + urls

    def update_stock(self, request):
        file_path = r'C:\Users\emill\Desktop\PTH Учусь\Дайбог создам сайт)\data.xlsx'
        update_stock_from_excel(file_path)
        self.message_user(request, "Остатки обновлены из Excel", messages.SUCCESS)
        return HttpResponseRedirect("../")  # Возврат на страницу списка

    
admin.site.register(Gallery)
