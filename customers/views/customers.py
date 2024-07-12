from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from tablib import Dataset

from customers.admin import CustomerResource
from customers.forms import CustomerModelForm, Customer, ImportForm, ExportForm


def customers(request):
    search = request.GET.get('search_query')
    page_num = request.GET.get('page')

    if search:
        all_customers = Customer.objects.filter(Q(name__icontains=search) | Q(country__icontains=search) |
                                                Q(city__icontains=search))
    else:
        all_customers = Customer.objects.all()

    item_list = all_customers.all()
    paginator = Paginator(item_list, 2)
    all_customers = paginator.get_page(page_num)

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


def export_data(request):
    if request.method == 'POST':
        form = ExportForm(request.POST)
        if form.is_valid():
            export_format = form.cleaned_data['export_format']
            resource = CustomerResource
            dataset = resource.export()

            if export_format == 'csv':
                response = HttpResponse(dataset.csv, content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
            elif export_format == 'xlsx':
                response = HttpResponse(dataset.xlsx,
                                        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="exported_data.xlsx"'
            elif export_format == 'json':
                response = HttpResponse(dataset.json, content_type='application/json')
                response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
            else:
                response = HttpResponse(status=400)

            return response
    else:
        form = ExportForm()

    return render(request, 'customers/customers.html', {'form': form})


def import_data(request):
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            dataset = Dataset()
            new_data = request.FILES['import_file']
            imported_data = dataset.load(new_data.read(), format='xlsx')  # Adjust the format as needed
            resource = CustomerResource()
            result = resource.import_data(dataset, dry_run=True)

            if not result.has_errors():
                resource.import_data(dataset, dry_run=False)
                return redirect('customers')

    else:
        form = ImportForm()

    return render(request, 'customers/customers.html', {'form': form})