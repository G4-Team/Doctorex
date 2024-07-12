from django.urls import include, path

from . import views

app_name = "account"

doctor_urls = [
    path("list/", views.DoctorListView.as_view(), name="doctors-list"),
]

urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("doctor/", include(doctor_urls), name="doctor"),
]
