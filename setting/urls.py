from django.urls import path

from . import views

app_name = "setting"

urlpatterns = [
    path("specialties/", views.SpecialtyListView.as_view(), name="specialties-list"),
]
