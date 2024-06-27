from django.urls import path
from app.views import index, detail, add_product

urlpatterns = [
    path('', index, name='index'),
    path('details/<int:product_id>', detail, name='detail'),
    path('index/', index, name='index'),
    path('add_product/', add_product, name='add_product')
]
