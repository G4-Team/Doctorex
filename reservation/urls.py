from django.urls import path, include
from . import views


app_name = "reservation"

comment_urls = [
    path('comment/', views.CommentView.as_view(), name='comment'),
    path('comment/<int:comment_id>', views.CommentEditView.as_view(), name='comment-edit'),
]

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/<str:search_content>', views.SearchView.as_view(), name='search'),
    path('', include(comment_urls)),
]