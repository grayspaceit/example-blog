from django.urls import path
from posts.views import *

urlpatterns = [

    path('list/', PostListView.as_view(),name='post_list'),
    path('post/detail/<int:pk>/',  PostDetailView.as_view(), name='post_detail'),
    path('post/new/',   CreatePostView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/',  PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/remove/',  PostDeleteView.as_view(), name='post_remove'),

    path('post/<int:pk>/comment/', add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/remove/',  comment_remove, name='comment_remove'),

    path('', post_list, name="post_list"),
    path('postdetail/<int:post_id>/', post_details, name='post_detail_json')
]
