from django import forms
from django.contrib.auth.models import Permission
from customers.models import Customer, User


class ImportForm(forms.Form):
    import_file = forms.FileField()


class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ()


class LoginForm(forms.Form):
    phone = forms.CharField(max_length=13)
    password = forms.CharField(max_length=255)

    def clean_phone(self):
        phone = self.data.get('phone')
        if not User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Number does not exist')
        return phone

    def clean_password(self):
        phone = self.cleaned_data.get('phone')
        password = self.data.get('password')
        try:
            user = User.objects.get(phone=phone)
            print(user)
            if not user.check_password(password):
                raise forms.ValidationError('Password did not match')
        except User.DoesNotExist:
            raise forms.ValidationError(f'{phone} does not exists')
        return password


class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(label='Password confirm', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'phone', 'password')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError(f'This {phone} is already registered')
        return phone

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

