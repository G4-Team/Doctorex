from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db.models import Avg
from django.shortcuts import render, redirect
from django.views import View

from .forms import RegisterForm, LoginForm
from .models import Doctor, Patient


class SignupView(View):
    def get(self, request):
        return render(request, "user/signup.html", )

    def post(self, request):
        form = RegisterForm(request.POST)

        if not form.is_valid():
            messages.error(request, form.errors)
            return render(request, 'user/signup.html', {'form': form})

        obj = form.save()
        Patient.objects.create(account=obj)
        return redirect('index')


class LoginView(View):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
        return render(request, 'user/login.html', {'form': form})


class DoctorListView(View):
    def get(self, request):
        from time import sleep

        sleep(20)
        doctors = Doctor.objects.annotate(
            average_score=Avg('visittime__reservation__comments__score')
        ).all().select_related("account", "specialty")
        context = {
            "doctors": doctors,
        }

        return render(
            request=request,
            template_name="user/partial/_doctors-list.html",
            context=context,
        )
