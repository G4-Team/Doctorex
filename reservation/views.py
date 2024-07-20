from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from setting.models import Specialty
from user.models import Doctor

from .forms import CommentForm
from .models import Comment, Reservation


class IndexView(View):
    def get(self, request):
        return render(request, "reservation/index.html")


class SerchView(View):
    def get(self, request):
        search = request.GET.get("search")
        print(search)

        specialties = Specialty.objects.filter(specialty__icontains=search)
        doctors = Doctor.objects.filter(
            Q(account__first_name__icontains=search)
            | Q(account__last_name__icontains=search)
        ).select_related("account")

        context = {
            "search": search,
            "specialties": specialties,
            "doctors": doctors,
        }
        from django.urls import reverse

        print(reverse("account:signup"))
        return render(
            request=request,
            template_name="reservation/search.html",
            context=context,
        )


class CommentView(View):
    form_class = CommentForm
    template_name = "reservation/comment-new.html"

    def get(self, request, doctor_id):
        reserved_times = Reservation.objects.filter(
            patient__account=request.user, visit_time__doctor__id=doctor_id
        ).all()
        return render(
            request,
            self.template_name,
            {
                "doctor_id": doctor_id,
                "reserved_times": reserved_times,
                "form": self.form_class,
            },
        )

    def post(self, request, doctor_id):
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.doctor_id = int(form.cleaned_data["doctor_id"])
            comment.author = request.user
            comment.reservation = get_object_or_404(
                Reservation, id=request.POST.get("time")
            )
            comment.save()
            messages.success(request, "نظر شما با موفقیت ثبت گردید")
            doctor = (
                Doctor.objects.select_related("specialty")
                .only(
                    "avg_rate",
                    "specialty__specialty",
                )
                .get(id=doctor_id)
            )
            comments = Comment.objects.filter(
                reservation__visit_time__doctor__id=doctor_id
            ).all()
            reserved_times = Reservation.objects.filter(
                patient__account=request.user, visit_time__doctor__id=doctor_id
            ).all()
            return render(
                request,
                self.template_name,
                {
                    "doctor_id": doctor_id,
                    "doctor": doctor,
                    "comments": comments,
                    "reserved_times": reserved_times,
                    "form": self.form_class,
                },
            )

        reserved_times = Reservation.objects.filter(
            patient__account=request.user, visit_time__doctor__id=doctor_id
        ).all()
        return render(
            request,
            self.template_name,
            {
                "doctor_id": doctor_id,
                "reserved_times": reserved_times,
                "form": form,
            },
        )


class CommentEditView(View):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)

        if comment.author != request.user:
            return redirect("index")

        return render(
            request,
            "reservation/comment-edit.html",
            {"comment": comment},
        )

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)

        if comment.author != request.user:
            return redirect("index")

        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():
            form.save()
            return redirect("index")

        print(form.errors)
        return render(
            request,
            "reservation/comment-edit.html",
            {"comment": comment},
        )
