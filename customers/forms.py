from django import forms
from django.contrib.auth.models import Permission
from django.core.mail import send_mail

from customers.models import Customer, User


class ImportForm(forms.Form):
    import_file = forms.FileField()


class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ()


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(max_length=255)

    def clean_email(self):
        email = self.data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email does not exist')
        return email

    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = self.data.get('password')
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise forms.ValidationError('Password did not match')
        except User.DoesNotExist:
            raise forms.ValidationError(f'{email} does not exists')
        return password


class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(label='Password confirm', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'This {email} is already registered')
        return email

    def clean_password(self):
        password1 = self.data.get('password')
        password2 = self.data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Passwords did not match')
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def send_email(self, user):
        token = user.profile.activation_token
        activation_link = f"http://127.0.0.1:8000/activate/{token}"

        send_mail(
            subject="Account Activation",
            message=f"Please click the following link to activate your account: {activation_link}",
            from_email='python3526@gmail.com',
            recipient_list=[user.email],
            fail_silently=False,
        )


class UserModelForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = User
        exclude = ()

    def save(self, commit=True):
        user = super(UserModelForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            self.save_m2m()
        return user
