from django.contrib import messages
from django.db.models import Avg
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from user.models import Doctor

from .forms import CommentForm
from .models import Comment, Reservation


class IndexView(View):
    def get(self, request):
        return render(request, "reservation/index.html")


class SearchView(View):
    def get(self, request, search_content):
        doctors = (
            Doctor.objects.filter(account__first_name__icontains=search_content)
            | Doctor.objects.filter(specialty__specialty__icontains=search_content)
            | Doctor.objects.filter(account__last_name__icontains=search_content)
        )
        doctors.annotate(average_score=Avg("visittime__reservation__comments__score"))
        return render(request, "reservation/search.html", {"doctors": doctors})


class CommentView(View):
    def post(self, request):
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
            previous_url = request.META.get("HTTP_REFERER")
            return HttpResponseRedirect(previous_url)


class CommentEditView(View):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)

        if comment.author != request.user:
            return redirect("index")

        return render(request, "comment.html", {"comment": comment})

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)

        if comment.author != request.user:
            return redirect("index")

        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():
            form.save()
            return redirect("index")

        print(form.errors)
        return render(request, "comment.html", {"comment": comment})
