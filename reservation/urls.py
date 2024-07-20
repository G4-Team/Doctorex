from django.urls import include, path

from . import views

comment_urls = [
    path("new-comment/<int:doctor_id>/", views.CommentView.as_view(), name="comment"),
    path(
        "comment/<int:comment_id>", views.CommentEditView.as_view(), name="comment-edit"
    ),
]

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("search/", views.SerchView.as_view(), name="search"),
    path("", include(comment_urls)),
]
