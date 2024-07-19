from django.db.models import Q
from django.shortcuts import render
from django.views import View

from setting.models import Specialty
from user.models import Doctor


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
