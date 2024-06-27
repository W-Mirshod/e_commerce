from django.urls import path

from customers.views.customers import customers, customer_detail, add_customer, edit_customer, delete_customer, \
    filter_page, sort_by_id, sort_by_id_desc, sort_by_name, sort_by_date
from customers.views.auth import login_page, logout_page, sign_up

urlpatterns = [
    path('customers/', customers, name='customers'),
    path('customer_details/<int:customer_id>', customer_detail, name='customer_detail'),
    path('add_customer/', add_customer, name='add_customer'),
    path('delete_customer/<int:customer_id>', delete_customer, name='del_customer'),
    path('edit_customer/<int:customer_id>', edit_customer, name='edit_customer'),
    path('filter_page/', filter_page, name='filter_page'),
    path('sort_by/sort_by_id', sort_by_id, name='sort_by_id'),
    path('sort_by/sort_by_id_desc', sort_by_id_desc, name='sort_by_id_desc'),
    path('sort_by/sort_by_name', sort_by_name, name='sort_by_name'),
    path('sort_by/sort_by_date', sort_by_date, name='sort_by_date'),

    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('register/', sign_up, name='register'),
]
