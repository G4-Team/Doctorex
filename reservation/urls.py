from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('/search/<string:search_content>', views.SearchView.as_view(), name='search'),
]