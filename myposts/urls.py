from os import name
#from django.conf.urls import url
from django.urls import path
from . import views
from .views import (
   PostCreateView, PostListView, PostUpdateView,
   PostDeleteView, MyPostsView,
   FollowingView, FollowersView, GalleryView, 
   ProfileCreateView, ProfileEditView, ProfileDeleteView, UserProfileView
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
   path('createprofile/', ProfileCreateView.as_view(), name='createprofile'),
   path('editprofile/<int:pk>', ProfileEditView.as_view() ,name='editprofile'),
   path('deleteprofile/<int:pk>',ProfileDeleteView.as_view(),name='deleteprofile'),
   path('userprofile/',UserProfileView.as_view(),name='userprofile'),
]
