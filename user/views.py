from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from user.models import Account

from .forms import RegisterForm
from .models import Doctor


class SignupView(View):
    form_class = RegisterForm
    template_name = "user/signup.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Account.objects.create_user(
                cd["email"],
                cd["username"],
                cd["first_name"],
                cd["last_name"],
                cd["password1"],
            )
            messages.success(
                request,
                "حساب کاربری با موفقیت ایجاد شد. پس از تأیید مدیریت، امکان ورود به سایت را خواهید داشت.",
                "success",
            )
            return redirect("index")
        return render(request, self.template_name, {"form": form})


class DoctorListView(View):
    def get(self, request):
        from time import sleep

        sleep(2)
        doctors = Doctor.objects.all().select_related("account", "specialty")
        context = {
            "doctors": doctors,
        }

        return render(
            request=request,
            template_name="user/partial/_doctors-list.html",
            context=context,
        )


class LoginView(View):
    pass
