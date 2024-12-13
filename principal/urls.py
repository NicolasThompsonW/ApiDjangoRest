from .views import (
    NewPostView,
    PostGetAllView,
    UpdatePostView,
    DeletePostView,
    GetPostView,
    CommentCreateView,
    CommentDeleteView,
    CommentUpdateView,
)
from django.urls import path

urlpatterns = [
    path("post/", NewPostView.as_view(), name="post"),
    path("posts/", PostGetAllView.as_view(), name="get_posts"),
    path("post/<int:pk>/", UpdatePostView.as_view(), name="update_post"),
    path("post/<int:pk>/delete/", DeletePostView.as_view(), name="delete_post"),
    path("post/<int:pk>/get/", GetPostView.as_view(), name="get_post"),
    path("comment/", CommentCreateView.as_view(), name="comment-create"),
    path("comment/<int:pk>/", CommentUpdateView.as_view(), name="comment-update"),
    path("comment/<int:pk>/delete/",
         CommentDeleteView.as_view(), name="comment-delete"),
]
