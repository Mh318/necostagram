from os import name
#from django.conf.urls import url
from django.urls import path
from . import views
from .views import (
   PostCreateView, PostListView, PostUpdateView,PostDetailView,
   PostDeleteView, MyPostsView,
   FollowingView, FollowersView, GalleryView, UserProfileView,
   CommentCreate,CommentDeleteView
)
app_name = 'myposts'
urlpatterns = [
   path('create/', PostCreateView.as_view(), name='create'),
   path('postlist/', PostListView.as_view(), name='postlist'),
   path('update/<int:pk>', PostUpdateView.as_view(), name='update'),
   path('delete/<int:pk>', PostDeleteView.as_view(), name='delete'),
   path('myposts/', MyPostsView.as_view(), name='myposts'),
   path('add_favourite/<int:pk>/', views.add_favourite, name='add_favourite'),
   path('rm_favourite/<int:pk>/', views.remove_favourite, name='rm_favourite'), 
   path('follower/', FollowersView.as_view(), name='follower'), 
   path('following/', FollowingView.as_view(), name='following'),
   path('gallery/', GalleryView.as_view(), name='gallery'), 
   path('add_file/', views.add_file, name='add_file'),
   path('postdetail/<int:pk>/', PostDetailView.as_view(), name='postdetail'),
   path('comment/create/<int:pk>/', CommentCreate.as_view(), name='comment_create'), 
   path('delete_comment/<int:pk>', CommentDeleteView.as_view(), name='delete_comment'),
   path('userprofile/',UserProfileView.as_view(),name='userprofile'),
]