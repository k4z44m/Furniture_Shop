from django.contrib import admin
from .models import Category, Product, Gallery
from django.utils.safestring import mark_safe


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'get_product_count']
    list_display_links = ['id', 'title']
    prepopulated_fields = {'slug': ['title']}

    def get_product_count(self, obj):
        if obj.products:
            try:
                return str(obj.products.all().count())
            except:
                return '0'
        else:
            return '0'

    get_product_count.short_description = 'Кол-во товаров'

class GalleryAdmin(admin.TabularInline):
    model = Gallery
    fk_name = 'product'
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'price', 'quantity', 'get_product_preview']
    list_display_links = ['id', 'title']
    list_editable = ['price', 'quantity']
    prepopulated_fields = {'slug': ['title']}
    inlines = [GalleryAdmin]
    list_filter = ['category', 'price']

    def get_product_preview(self, obj):
        if obj.images:
            try:
                return mark_safe(f'<img src="{obj.images.first().image.url}" width="75">')
            except:
                return '-'
        else:
            return '-'
