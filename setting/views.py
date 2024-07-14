from django.db.models import Count
from django.shortcuts import render
from django.views import View

from user.models import Doctor

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


class SpecialtyView(View):
    def get(self, request, slug):
        specialty = Specialty.objects.get(slug=slug)
        doctors = Doctor.objects.filter(specialty__id=specialty.id).select_related(
            "account"
        )
        context = {
            "specialty": specialty,
            "doctors": doctors,
        }
        return render(
            request=request,
            template_name="setting/specialty.html",
            context=context,
        )
