from django import forms
from django.core.exceptions import ValidationError

from user.models import Account


class RegisterForm(forms.Form):
    GENDERS = {"M": "آقا", "F": "خانم"}
    gender = forms.CharField(widget=forms.RadioSelect(choices=GENDERS.items()), label='جنسیت')
    first_name = forms.CharField(label='نام', min_length=3, max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    last_name = forms.CharField(label='نام خانوادگی', min_length=3, max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    email = forms.EmailField(label='ایمیل', min_length=3, max_length=50, widget=forms.EmailInput(
        attrs={'class': 'form-control'}
    ))
    password1 = forms.CharField(label='گذرواژه', min_length=6, max_length=50, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))
    password2 = forms.CharField(label='تکرار گذرواژه', min_length=6, max_length=50, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))
    username = forms.CharField(label='نام کاربری', min_length=3, max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = Account.objects.filter(email=email).exists()
        if user:
            raise ValidationError('این ایمیل پیش از این استفاده شده است!')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        user = Account.objects.filter(username=username).exists()
        if user:
            raise ValidationError('این نام کاربری تکراری است!')
        return username

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError('گذرواژه های وارد شده با یکدیگر همخوانی ندارند!')


class SigninForm(forms.Form):
    email = forms.EmailField(label='ایمیل', min_length=3, max_length=50, widget=forms.EmailInput(
        attrs={'class': 'form-control'}
    ))
    password = forms.CharField(label='گذرواژه', min_length=6, max_length=50, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'phone_number']
