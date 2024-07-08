from django.shortcuts import render
from django.views import View
from .forms import RegisterForm
class SignupView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'user/signup.html', {'form': form})