from itertools import count

from django.db.models import Min, Max, Avg, Count
from django.shortcuts import render, redirect
from django.views import View
from app.forms import ProductForm
from app.models import Product
from customers.models import Customer


class StaticsPage(View):
    def get(self, request):
        products = Product.objects.all()
        min_price_results = Product.objects.annotate(min_=Min("price"))
        min_price = (min_price_results.aggregate(min_price=Min("price"))['min_price']) // 20
        a_min_price = min_price * 20

        max_price_results = Product.objects.annotate(max_=Max("price"))
        max_price = (max_price_results.aggregate(max_price=Max("price"))['max_price']) // 20
        a_max_price = max_price * 20
        average_price_results = Product.objects.annotate(avg=Avg("price"))
        average_price = (average_price_results.aggregate(avg_price=Avg("price"))['avg_price']) // 20
        a_average_price = average_price * 20

        counting_result = Customer.objects.annotate(count=Count('id'))
        customers_count = counting_result.aggregate(count=Count('id'))['count']
        customers_count_st = customers_count * 10

        context = {'Products': products,
                   'min_price_st': min_price,
                   'min_price': a_min_price,
                   'max_price_st': max_price,
                   'max_price': a_max_price,
                   'average_price_st': average_price,
                   'average_price': a_average_price,
                   'customers_count': customers_count,
                   'customers_count_st': customers_count_st,
                   'temp': 20}
        return render(request, 'statics.html', context)


def index(request):
    products = Product.objects.all().order_by('-id')
    context = {'Products': products}
    return render(request, 'app/product-list.html', context)


def detail(request, product_id):
    products = Product.objects.get(id=product_id)
    attributes = products.get_attributes()
    context = {'Products': products,
               'Attributes': attributes}
    return render(request, 'app/product-details.html', context)


def index2(request):
    return render(request, 'app/index.html')


def add_product(request):
    if request.method == 'POST':
        form1 = ProductForm(request.POST)
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        discount = request.POST['discount']
        product = Product(name=name, description=description, price=price, discount=discount)
        if form1.is_valid():
            product.save()
            return redirect('index')

    else:
        form1 = ProductForm()

    context = {'form1': form1}
    return render(request, 'app/add_product.html', context)
