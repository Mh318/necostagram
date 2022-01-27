from re import template
import re
from django.db.models.fields.files import ImageField
from django.http import request, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Gallery, Profile
from .forms import PostCreateForm, PostUpdateForm, ProfileCreateForm, ProfileEditForm #追加
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, query
from accounts.models import Relationship,User
from myposts import models

from functools import reduce
from operator import and_

class PostCreateView(LoginRequiredMixin, CreateView):
	template_name = 'myposts/create.html'
	form_class = PostCreateForm
	success_url = reverse_lazy('myposts:create')

	def form_valid(self, form):
		# formに問題なければ、owner id に自分のUser idを割り当てる     
		# request.userが一つのセットでAuthenticationMiddlewareでセットされている。
		form.instance.owner_id = self.request.user.id
		messages.success(self.request, 'Done')
		return super(PostCreateView, self).form_valid(form)
		
	def form_invalid(self, form):
		messages.warning(self.request, 'Failed')
		return redirect('myposts:create')
	
	def newPost(request):
		if request.method == "POST":
			form = PostCreateForm(request.POST)
			if form.is_valid():
				post = Post()
				print(request)
				post.photo = request.FILES['photo']
				post.save()
				return redirect('myposts:myposts')
		else:
			form = PostCreateForm()
		return render(request, 'myposts/create.html',{'form':form})


class PostListView(LoginRequiredMixin, ListView):
	template_name = 'myposts/postlist.html'
	model = Post
	paginate_by = 12

# Postsテーブルの全データを取得するメソッド定義
# テンプレートでは、object_listとしてreturnの値が渡される
	def get_queryset(self):
		word = self.request.GET.get('keyword')

		if word:
			object_list = Post.objects.filter(
				Q(comment__icontains=word)
			)
		else:
			object_list = Post.objects.all()
		return object_list

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = self.request.user
		context['favourite_list'] = user.favourite_post.all()

		return context

def add_favourite(request, pk):
   # postのpkをhtmlから取得
   post = get_object_or_404(Post, pk=pk)
   # ログインユーザーを取得
   user = request.user
   # ログインユーザーをfavoritePostのUser_idとして、post_idは
   # 上で取得したPostを記録
   user.favourite_post.add(post)
   return redirect('myposts:postlist')

def remove_favourite(request, pk):
   # postのpkをhtmlから取得
   post = get_object_or_404(Post, pk=pk)
   # ログインユーザーを取得
   user = request.user
   # ログインユーザーをfavoritePostのUser_idとして、post_idは
   # 上で取得したPostを記録
   user.favourite_post.remove(post)
   return redirect('myposts:postlist')

class PostUpdateView(LoginRequiredMixin, UpdateView): 
	model = Post
	form_class = PostUpdateForm
	template_name = 'myposts/update.html'
	def form_valid(self, form):
		messages.success(self.request, '更新が完了しました')
		return super(PostUpdateView, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('myposts:update', kwargs={'pk': self.object.id})  
		
	def form_invalid(self, form):
		messages.warning(self.request, '更新が失敗しました')
		return reverse_lazy('myposts:update', kwargs={'pk': self.object.id})

class PostDeleteView(LoginRequiredMixin, DeleteView):
	model = Post
	template_name = 'myposts/delete.html'

# deleteviewでは、SuccessMessageMixinが使われないので設定する必要あり
	success_url = reverse_lazy('myposts:myposts')
	success_message = "投稿は削除されました。"
# 削除された際にメッセージが表示されるようにする。
	def delete(self, request, *args, **kwargs):
		messages.success(self.request, self.success_message)
		return super(PostDeleteView, self).delete(request, *args, **kwargs)

class MyPostsView(LoginRequiredMixin, ListView):
# テンプレートを指定
	template_name = 'myposts/myposts.html'
# 利用するモデルを指定
	model = Post
# ページネーションの表示件数
	paginate_by = 6

# Postsテーブルのowner_idが自分自身の全データを取得するメソッド定義
	def get_queryset(self):
		qs = Post.objects.filter(owner_id=self.request.user)
		return qs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = self.request.user

		qs = Post.objects.filter(owner_id=self.request.user)
		# qsのレコード数をmy_posts_countというコンテキストとして設定
		context['my_posts_count'] = qs.count()
		# Postsテーブルの全データを取得しpost_listへ格納
		context['favourite_list'] = user.favourite_post.all()
		context['following_list'] = Relationship.objects.filter(follower_id=user.id)
		# 自分がfollowしているidのみをmy_follow_listとして取得
		context['my_follow_list'] = (Relationship.objects.filter(follower_id=user.id)).values_list('following_id', flat=True)
		# 自分がフォローしている人をfollowingsとして取得
		followings = (Relationship.objects.filter(follower_id=user.id)).values_list('following_id')
		context['following_count'] = User.objects.filter(id__in=followings).count()
		# 自分をフォローしている人をfollowersとして取得
		followers = (Relationship.objects.filter(following_id=user.id)).values_list('follower_id')
		# context['followers_data] = User.objects.filter(id__in=followers).count()
		context['follower_count'] = followers.count()
		return context

class FollowersView(LoginRequiredMixin, ListView):
   # テンプレートを指定
   template_name = 'myposts/followers.html'
   # 利用するモデルを指定
   model = Relationship

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       user = self.request.user
       # Postsテーブルの自分の投稿数をmy_posts_countへ格納
       context['my_posts_count'] = Post.objects.filter(owner_id=self.request.user).count()
       # 自分がフォローしている人をfollowingsとして取得
       followings = (Relationship.objects.filter(follower_id=user.id)).values_list('following_id')
       # 自分がフォローしている人のオブジェクトを取得
       context['following_list'] = User.objects.filter(id__in=followings)
       # 自分がフォローしている人の数を取得
       context['following_count'] = User.objects.filter(id__in=followings).count()
       # 自分をフォローしている人をfollowersとして取得
       followers = (Relationship.objects.filter(following_id=user.id)).values_list('follower_id')
       # 自分をフォローしている人の数を取得
       context['follower_list'] = User.objects.filter(id__in=followers)
       return context

class FollowingView(LoginRequiredMixin, ListView):
   # テンプレートを指定
   template_name = 'myposts/followings.html'
   # 利用するモデルを指定
   model = Relationship

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       user = self.request.user
       # Postsテーブルの自分の投稿数をmy_posts_countへ格納
       context['my_posts_count'] = Post.objects.filter(owner_id=self.request.user).count()
       # 自分がフォローしている人をfollowingsとして取得
       followings = (Relationship.objects.filter(follower_id=user.id)).values_list('following_id')
       # 自分がフォローしている人のオブジェクトを取得
       context['following_list'] = User.objects.filter(id__in=followings)
       # 自分をフォローしている人をfollowersとして取得
       followers = (Relationship.objects.filter(following_id=user.id)).values_list('follower_id')
       # 自分をフォローしている人の数を取得
       context['follower_count'] = User.objects.filter(id__in=followers).count()
       return context

# file(=画像)をアップロードする関数
def add_file(request):
   if request.method == "POST":        
       # ログインユーザーを取得
       user = request.user
       # 画像をテンプレートからfileとして取得
       pict = request.FILES.get('file')
       # Galleryモデルにオーナーと画像を保存
       Gallery.objects.create(owner = user, image=pict)
       return HttpResponse('')
   return HttpResponse('post error')
   
class GalleryView(LoginRequiredMixin,ListView):
   template_name = 'myposts/gallery.html'
   # 利用するモデルを指定
   model = Gallery    
   
   # Galleryテーブルのowner_idが自分自身の全データを取得するqs
   def get_queryset(self):  
       qs = Gallery.objects.filter(owner_id=self.request.user)
       return qs

class ProfileCreateView(LoginRequiredMixin, CreateView):
	template_name = 'myposts/createprofile.html'
	form_class = ProfileCreateForm
	success_url = reverse_lazy('myposts:createprofile')

	def form_valid(self, form):
		# formに問題なければ、owner id に自分のUser idを割り当てる     
		# request.userが一つのセットでAuthenticationMiddlewareでセットされている。
		form.instance.owner_id = self.request.user.id
		messages.success(self.request, 'Done')
		return super(ProfileCreateView, self).form_valid(form)
		
	def form_invalid(self, form):
		messages.warning(self.request, 'Failed')
		return redirect('myposts:createprofile')

	def profilePost(request):
		if request.method == "POST":
			form = ProfileCreateForm(request.POST)
			if form.is_valid():
				post = Profile()
				print(request)
				post.avatar = request.FILES['アイコン画像']
				post.save()
				return redirect('myposts:myposts')
		else:
			form = ProfileCreateForm()
		return render(request, 'myposts/createprofile.html',{'form':form})


class ProfileEditView(LoginRequiredMixin, UpdateView):
	model = Profile
	form_class = ProfileEditForm
	template_name = 'myposts/editprofile.html'

	def form_valid(self, form):
		messages.success(self.request, '更新が完了しました')
		return super(ProfileEditView, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('myposts:editprofile', kwargs={'pk': self.object.id})  
		
	def form_invalid(self, form):
		messages.warning(self.request, '更新が失敗しました')
		return reverse_lazy('myposts:editprofile', kwargs={'pk': self.object.id})

class ProfileDeleteView(LoginRequiredMixin, DeleteView):
	model = Profile
	template_name = 'myposts/deleteprofile.html'

# deleteviewでは、SuccessMessageMixinが使われないので設定する必要あり
	success_url = reverse_lazy('myposts:myposts')
	success_message = "投稿は削除されました。"
# 削除された際にメッセージが表示されるようにする。
	def delete(self, request, *args, **kwargs):
		messages.success(self.request, self.success_message)
		return super(ProfileDeleteView, self).delete(request, *args, **kwargs)

class UserProfileView(LoginRequiredMixin,ListView):
	model = Profile
	template_name= 'myposts/userprofile.html'

	def get_queryset(self):
		return Profile.objects.all()
