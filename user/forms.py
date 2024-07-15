from django import forms

from .models import Account


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'first_name', 'last_name', 'email', 'password']


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'phone_number']
