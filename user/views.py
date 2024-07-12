from django.shortcuts import render
from django.views import View

from .forms import RegisterForm
from .models import Doctor


class SignupView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "user/signup.html", {"form": form})


class DoctorListView(View):
    def get(self, request):
        from time import sleep

        sleep(20)
        doctors = Doctor.objects.all().select_related("account", "specialty")
        context = {
            "doctors": doctors,
        }

        return render(
            request=request,
            template_name="user/partial/_doctors-list.html",
            context=context,
        )
