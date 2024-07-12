from django.db.models import Count
from django.shortcuts import render
from django.views import View

from .models import Specialty


class SpecialtyListView(View):
    def get(self, request):
        from time import sleep

        sleep(2)
        specialties = Specialty.objects.annotate(doctors_count=Count("doctors")).all()

        context = {
            "specialties": specialties,
        }
        return render(
            request=request,
            template_name="setting/_specialties.html",
            context=context,
        )
