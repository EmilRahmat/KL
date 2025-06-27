from django.contrib import admin
from django.utils.html import format_html
from goods.models import Categories,Products,Variation,Gallery
from django.utils.safestring import mark_safe
from django.urls import path
from django.http import HttpResponseRedirect
from django.contrib import messages
from .utils import update_stock_from_excel, update_stock_by_receipts, import_products_from_excel  # Импортируем функцию
from django.shortcuts import render
from django.core.files.storage import default_storage
import os
from .admin_forms import ExcelUploadForm
from django import forms

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
    list_display = ('pk', 'name', 'sku', 'price', 'get_variation_count', 'discount', 'get_photo', 'created_at', 'is_available')
    list_editable = ('price', 'discount', 'is_available')
    prepopulated_fields = {'slug':('sku',)}
    list_filter = ('category', 'price')
    list_display_links = ('name',)
    search_fields = ('name', 'sku', 'description')
    inlines = (GalleryInline, VariationInline)
    change_list_template = "admin/products_changelist.html"
    
    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path('import-products/', self.admin_site.admin_view(self.import_products), name='import-products'),
        ]
        return custom + urls

    def import_products(self, request):
        # 1) При POST — обрабатываем файл
        if request.method == 'POST':
            form = ExcelUploadForm(request.POST, request.FILES)
            if form.is_valid():
                # Сохраняем загруженный файл во временное хранилище
                tmp_path = default_storage.save('tmp/products.xlsx', request.FILES['excel_file'])
                tmp_file = os.path.join(default_storage.location, tmp_path)

                # Вызываем утилиту импорта
                logs = import_products_from_excel(tmp_file)

                # Выводим сообщения в админке
                for line in logs:
                    self.message_user(request, line)

                # После импорта — перенаправляем обратно в changelist
                return HttpResponseRedirect("../")
        else:
            # 2) При GET — показываем форму
            form = ExcelUploadForm()

        # Рендерим шаблон с формой
        context = dict(
            self.admin_site.each_context(request),
            form=form,
        )
        return render(request, "admin/import_products.html", context)
    
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
    list_display = ('product', 'sku', 'size', 'producer_size', 'quantity', 'is_active')
    list_editable = ('is_active', 'quantity', 'size')
    list_filter = ('product', 'size', 'producer_size')
    search_fields = ('product__product_name',)
    prepopulated_fields = {'sku': ('sku',)}
    change_list_template = "admin/variation_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('update-stock/', self.admin_site.admin_view(self.update_stock), name='goods_variation_update_stock'),
            path('update-stock-receipts/', self.admin_site.admin_view(self.update_stock_by_receipts), name='goods_variation_update_stock_receipts'),
        ]
        return custom_urls + urls


    def update_stock(self, request):
        file_path = r'C:\Users\emill\Desktop\PTH Учусь\Дайбог создам сайт)\Обновление остатков товаров.xlsx'
        update_stock_from_excel(file_path)
        self.message_user(request, "Остатки обновлены из Excel", messages.SUCCESS)
        return HttpResponseRedirect("../")

    def update_stock_by_receipts(self, request):
        file_path = r'C:\Users\emill\OneDrive\Резервная копия\Продажи товаров.xlsx'
        update_stock_by_receipts(file_path)
        self.message_user(request, "Остатки обновлены по чекам", messages.SUCCESS)
        return HttpResponseRedirect("../")
    
admin.site.register(Gallery)
