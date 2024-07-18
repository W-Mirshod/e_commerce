from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from customers.admin import CustomerResource
from customers.forms import CustomerModelForm
from customers.models import Customer


class CustomerView(View):
    def get(self, request):
        search = request.GET.get('search_query')
        page_num = request.GET.get('page')

        if search:
            all_customers = Customer.objects.filter(Q(full_name__icontains=search) | Q(email__icontains=search))
        else:
            all_customers = Customer.objects.all()

        item_list = all_customers.all()
        paginator = Paginator(item_list, 2)

        try:
            all_customers = paginator.page(page_num)
        except PageNotAnInteger:
            all_customers = paginator.page(1)
        except EmptyPage:
            all_customers = paginator.page(paginator.num_pages)

        context = {'Customers': all_customers}

        return render(request, 'customers/customers.html', context)


class CustomerDetailView(View):
    def get(self, request, customer_id):
        customer = get_object_or_404(Customer, id=customer_id)
        context = {'customer': customer}
        return render(request, 'customers/customer-details.html', context)


class AddCustomerView(View):
    def get(self, request):
        form = CustomerModelForm()
        return render(request, 'customers/add_customer.html', {'Form': form})

    def post(self, request):
        form = CustomerModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customers')
        return render(request, 'customers/add_customer.html', {'Form': form})


class DeleteCustomerView(View):
    def get(self, request, customer_id):
        customer = get_object_or_404(Customer, id=customer_id)
        customer.delete()
        return redirect('customers')


class EditCustomerView(View):
    def get(self, request, customer_id):
        customer = get_object_or_404(Customer, id=customer_id)
        form = CustomerModelForm(instance=customer)
        return render(request, 'customers/edit_customer.html', {'form': form})

    def post(self, request, customer_id):
        customer = get_object_or_404(Customer, id=customer_id)
        form = CustomerModelForm(data=request.POST, files=request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customers')


class ExportingCustomersView(View):
    def get(self, request):
        resource = CustomerResource()
        dataset = resource.export()

        if request.GET.get('export_options') == 'csv':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="my_model_data.csv"'
        elif request.GET.get('export_options') == 'xlsx':
            response = HttpResponse(dataset.xlsx,
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="my_model_data.xlsx"'
        elif request.GET.get('export_options') == 'json':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="my_model_data.json"'
        elif request.GET.get('export_options') == 'yaml':
            response = HttpResponse(dataset.yaml, content_type='application/x-yaml')
            response['Content-Disposition'] = 'attachment; filename="my_model_data.yaml"'
        else:
            return HttpResponseBadRequest("Unsupported format.")

        return response

    def render_to_response(self, context):
        return render(self.request, 'customers/customers.html', context)


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
