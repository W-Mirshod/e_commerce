from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from customers.forms import UserModelForm
from customers.models import Customer, User

admin.site.index_title = "Admin's Page"
admin.site.site_title = "Smth"
admin.site.site_header = "E-Commerce"


class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer
        exclude = ()


@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = CustomerResource

    list_display = ('id', 'full_name', 'email', 'joined', 'address', 'is_active')
    search_fields = ('id', 'full_name', 'phone')
    list_filter = ('id', 'full_name')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserModelForm
    list_display = ('id', 'username', 'phone', 'is_active')
    search_fields = ('id', 'username', 'phone')
    list_filter = ('id', 'username')
