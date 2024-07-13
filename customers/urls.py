from django.urls import path

from customers.views.customers import CustomerView, CustomerDetailView, AddCustomerView, EditCustomerView, \
    DeleteCustomerView, filter_page, sort_by_id, sort_by_id_desc, sort_by_name, sort_by_date, ExportingCustomersView
from customers.views.auth import login_page, logout_page, sign_up

urlpatterns = [
    path('customers/', CustomerView.as_view(), name='customers'),
    path('customer_details/<int:customer_id>', CustomerDetailView.as_view(), name='customer_detail'),
    path('add_customer/', AddCustomerView.as_view(), name='add_customer'),
    path('delete_customer/<int:customer_id>', DeleteCustomerView.as_view(), name='del_customer'),
    path('edit_customer/<int:customer_id>', EditCustomerView.as_view(), name='edit_customer'),
    path('filter_page/', filter_page, name='filter_page'),
    path('sort_by/sort_by_id', sort_by_id, name='sort_by_id'),
    path('sort_by/sort_by_id_desc', sort_by_id_desc, name='sort_by_id_desc'),
    path('sort_by/sort_by_name', sort_by_name, name='sort_by_name'),
    path('sort_by/sort_by_date', sort_by_date, name='sort_by_date'),
    path('exporting/', ExportingCustomersView.as_view(), name='export_data'),

    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('register/', sign_up, name='register'),
]
