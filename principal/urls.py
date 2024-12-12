from .views import NewPostView, PostGetAllView, UpdatePostView, DeletePostView, GetPostView
from django.urls import path

urlpatterns = [
    path('post/', NewPostView.as_view(), name='post'),
    path('posts/', PostGetAllView.as_view(), name='get_posts'),
    path('post/<int:pk>/', UpdatePostView.as_view(), name='update_post'),
    path('post/<int:pk>/delete/', DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/get/', GetPostView.as_view(), name='get_post'),
    
]