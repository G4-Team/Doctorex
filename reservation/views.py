from django.shortcuts import render
from django.views import View

from user.models import Doctor


class IndexView(View):
    def get(self, request):
        return render(request, "reservation/index.html")


class SearchView(View):
    def get(self, request, search_content):
        doctors = (Doctor.objects.filter(account__first_name__icontains=search_content) |
                   Doctor.objects.filter(specialty__specialty__icontains=search_content) |
                   Doctor.objects.filter(account__last_name__icontains=search_content))
        return render(request, "reservation/search.html", {"doctors": doctors})
