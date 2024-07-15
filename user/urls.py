from django.urls import include, path

from . import views

app_name = "account"

doctor_urls = [
    path("list/", views.DoctorListView.as_view(), name="doctors-list"),
]

urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path("doctor/", include(doctor_urls), name="doctor"),
    path('signout', views.SignoutView.as_view(), name='signout'),
]
