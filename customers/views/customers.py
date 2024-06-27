from django.db.models import Q
from django.shortcuts import render, redirect

from customers.forms import CustomerModelForm, Customer


# Create your views here.

def customers(request):
    search = request.GET.get('search_query')
    if search:
        all_customers = Customer.objects.filter(Q(name__icontains=search) | Q(country__icontains=search) |
                                                 Q(city__icontains=search))
    else:
        all_customers = Customer.objects.all()

    context = {'Customers': all_customers}
    return render(request, 'customers/customers.html', context)


def customer_detail(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    context = {'customer': customer}
    print(context)
    return render(request, 'customers/customer-details.html', context)


def add_customer(request):
    form = CustomerModelForm()
    if request.method == 'POST':
        form = CustomerModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customers')

    context = {'Form': form}
    return render(request, 'customers/add_customer.html', context)


def delete_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    customer.delete()
    return redirect('customers')


def edit_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    form = CustomerModelForm(instance=customer)
    if request.method == 'POST':
        form = CustomerModelForm(data=request.POST, files=request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customers')

    context = {'form': form}

    return render(request, 'customers/edit_customer.html', context)


def filter_page(request):
    sorts = ['Id_Inc', 'Id_Decs']
    context = {'Sorts': sorts}
    return render(request, 'customers/filter.html', context)


def sort_by_id(request):
    customer1 = Customer.objects.all()
    context = {'Customers': customer1}
    return render(request, 'customers/customers.html', context)


def sort_by_id_desc(request):
    customer1 = Customer.objects.all().order_by('-id')
    context = {'Customers': customer1}
    return render(request, 'customers/customers.html', context)


def sort_by_name(request):
    customer1 = Customer.objects.all().order_by('name')
    context = {'Customers': customer1}
    return render(request, 'customers/customers.html', context)


def sort_by_date(request):
    customer1 = Customer.objects.all().order_by('created_date')
    context = {'Customers': customer1}
    return render(request, 'customers/customers.html', context)
