from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from customers.forms import LoginForm, RegistrationForm
from customers.models import User


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            user = authenticate(request, phone=phone, password=password)
            print(user)
            if user:
                login(request, user)
                return redirect('customers')
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})


def logout_page(request):
    if request.method == 'GET':
        logout(request)
        return redirect('customers')
    return render(request, 'auth/logout.html')


def sign_up(request):
    if request.method == 'POST':
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            user.save()
            login(request, user)
            return redirect('customers')

    else:
        register_form = RegistrationForm()

    return render(request, 'auth/register.html', {'form': register_form})
