from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from reservation.models import Comment, VisitTime, Reservation
from .forms import RegisterForm, LoginForm, UserForm
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

        sleep(5)
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


class ProfileView(View):
    def get(self, request):
        return render(request, 'user/profile.html')

    def post(self, request):
        form = UserForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('index')
        print(form.errors)
        return render(request, 'user/profile.html', {'form': form})


class DoctorDetailView(View):
    def get(self, request, id: int):
        doctor = Doctor.objects.annotate(
            average_score=Avg('visittime__reservation__comments__score')
        ).get(id=id)
        times = VisitTime.objects.filter(doctor=doctor, is_reserved=False).all()
        reserved_times = Reservation.objects.filter(patient__account=request.user,
                                                    visit_time__doctor=doctor).all()
        comments = Comment.objects.filter(reservation__visit_time__doctor=doctor).all()

        return render(request, 'user/doctor.html',
                      {'doctor': doctor, 'times': times, 'reserved_times': reserved_times, 'comments': comments})

    def post(self, request, id: int):
        user = request.user
        visit_time_id = request.POST.get('time')
        visit_time = get_object_or_404(VisitTime, id=visit_time_id)

        if user.balance < visit_time.doctor.visit_cost:
            return redirect('balance')

        user.balance -= visit_time.doctor.visit_cost
        visit_time.doctor.account.balance += visit_time.doctor.visit_cost
        user.save()
        visit_time.doctor.save()

        patient = get_object_or_404(Patient, account=user)
        Reservation.objects.create(patient=patient, visit_time=visit_time)
        visit_time.is_reserved = True
        visit_time.save()

        messages.success(request, 'رزرو شما با موفقیت انجام شد!')
        return redirect('index')
