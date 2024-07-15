from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from reservation.models import Comment, Reservation
from user.models import Account, Patient

from .forms import RegisterForm, ProfileForm
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

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        user = request.user
        form = ProfileForm(instance=user)
        comments = Comment.objects.filter(author=user)

        return render(request, "user/profile.html", {"form": form,"comments": comments})
    def post(self, request):
        user = request.user
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        comments = Comment.objects.filter(author=user)
        return render(request, "user/profile.html", {"form": form, "comments": comments})

class ProfileVisitHistory(View):
    def get(self, request):
        user = request.user
        try:
            patient = Patient.objects.get(account=user)
            reservations = Reservation.objects.filter(patient=patient)
        except Patient.DoesNotExist:
            reservations = None
        return render(request, "user/visit_history.html", {"reservations":reservations})

class ProfileCommentView(View):
    def get(self, request):
        user = request.user
        comments = Comment.objects.filter(author=user)
        return render(request, "user/comments.html", {"comments": comments})
