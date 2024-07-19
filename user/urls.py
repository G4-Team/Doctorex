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
    path('verify-email/<slug:username>', views.VerifyEmailView.as_view(), name="verify-email"),
    path('resend-otp/', views.ResendOtpView.as_view(), name="resend-otp"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("visit_history/", views.ProfileVisitHistory.as_view(), name="visit_history"),
    path("comments/", views.ProfileCommentView.as_view(), name="comments"),
]
