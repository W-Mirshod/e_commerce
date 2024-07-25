from django.contrib import admin

from app.models import Product, Images, AttributeKey, AttributeValue, AttributeReference


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'discount', 'favoured')
    search_fields = ('name',)
    list_filter = ('id', 'price')


admin.site.register(Images)
admin.site.register(AttributeKey)
admin.site.register(AttributeValue)
admin.site.register(AttributeReference)
