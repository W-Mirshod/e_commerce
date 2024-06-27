from django.shortcuts import render, redirect
from app.forms import ProductForm
from app.models import Product


# Create your views here.
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
