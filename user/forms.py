from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', min_length=3, max_length=50)
    email = forms.EmailField(label='Email', min_length=3, max_length=50)
    password = forms.CharField(label='Password', min_length=6, max_length=50)