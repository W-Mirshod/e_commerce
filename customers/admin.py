from django.contrib import admin
from customers.models import Customer

admin.site.index_title = "Admin's Page"
admin.site.site_title = "Smth"
admin.site.site_header = "E-Commerce"


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'joined', 'address', 'is_active')
    search_fields = ('id', 'full_name', 'phone')
    list_filter = ('id', 'full_name')
