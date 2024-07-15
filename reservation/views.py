from django.contrib import messages
from django.db.models import Avg
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View

from user.models import Doctor
from .forms import CommentForm
from .models import Comment, Reservation


class IndexView(View):
    def get(self, request):
        return render(request, "reservation/index.html")


class SearchView(View):
    def get(self, request, search_content):
        doctors = (Doctor.objects.filter(account__first_name__icontains=search_content) |
                   Doctor.objects.filter(specialty__specialty__icontains=search_content) |
                   Doctor.objects.filter(account__last_name__icontains=search_content))
        doctors.annotate(average_score=Avg('visittime__reservation__comments__score'))
        return render(request, "reservation/search.html", {"doctors": doctors})


class CommentView(View):
    def post(self, request):
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.reservation = get_object_or_404(Reservation, id=request.POST.get('time'))
            comment.save()
            messages.success(request, 'نظر شما با موفقیت ثبت گردید')
            previous_url = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(previous_url)

        print(form.errors)
