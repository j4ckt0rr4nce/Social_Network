from django.urls import path
from .views import post_comment_create__and_list_view, like_unlike_post, PostDeleteView, PostUpdateView


app_name = 'posts'

urlpatterns = [
    path('post/', post_comment_create__and_list_view, name='post'),
    path('liked/', like_unlike_post, name='liked'),
    path('<pk>-delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<pk>-update/', PostUpdateView.as_view(), name='post-update'),
]