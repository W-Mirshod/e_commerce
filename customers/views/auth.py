import uuid
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView
from customers.forms import LoginForm, RegistrationForm
from customers.models import Profile


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'auth/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('customers')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('customers')


class SignUpView(CreateView):
    template_name = "auth/register.html"
    form_class = RegistrationForm
    success_url = "/customers/"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.save()

        Profile.objects.get_or_create(user=user)

        profile = user.profile
        profile.activation_token = str(uuid.uuid4())
        profile.save()

        form.send_email(user)
        return super().form_valid(form)


class ActivateView(View):
    def get(self, request, token):
        profile = get_object_or_404(Profile, activation_token=token)
        user = profile.user
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('customers')
