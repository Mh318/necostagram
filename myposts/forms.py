<<<<<<< HEAD
from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import Post, Profile

class PostCreateForm(forms.ModelForm):
   class Meta:
        model = Post
        fields = (
            'comment',
            'photo',
            'detail',
        )
        widgets = {
           'comment': forms.Textarea(
               attrs={'rows': 10, 'cols': 30,
                      'placeholder': 'ここに入力してください'}
            ),
        }
    

class PostUpdateForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = (
           'comment',
           'photo',
           'detail'
       )
       widgets = {
           'comment': forms.Textarea(
               attrs={'rows': 10, 'cols': 30}
           ),
       }
#追加
class FindForm(forms.Form):
    find = forms.CharField(label='Find', required=False, widget=forms.TextInput(attrs={'class':'form-control'}))


class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'avatar',
            'prof',
            'sato_oya',
        )
        widgets = {
            'prof':forms.Textarea(
                attrs={'rows': 10, 'cols': 30,
                'placeholder': 'ここに入力してください'}

            )
        }

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'avatar',
            'prof',
            'sato_oya',
        )
        widgets = {
            'prof':forms.Textarea(
                attrs={'rows': 10, 'cols': 30,}
            ),
=======
from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import Post, Profile

class PostCreateForm(forms.ModelForm):
   class Meta:
        model = Post
        fields = (
            'comment',
            'photo',
            'detail',
        )
        widgets = {
           'comment': forms.Textarea(
               attrs={'rows': 10, 'cols': 30,
                      'placeholder': 'ここに入力してください'}
            ),
        }
    

class PostUpdateForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = (
           'comment',
           'photo',
           'detail'
       )
       widgets = {
           'comment': forms.Textarea(
               attrs={'rows': 10, 'cols': 30}
           ),
       }
#追加
class FindForm(forms.Form):
    find = forms.CharField(label='Find', required=False, widget=forms.TextInput(attrs={'class':'form-control'}))


class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'avatar',
            'prof',
            'sato_oya',
        )
        widgets = {
            'prof':forms.Textarea(
                attrs={'rows': 10, 'cols': 30,
                'placeholder': 'ここに入力してください'}

            )
        }

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'avatar',
            'prof',
            'sato_oya',
        )
        widgets = {
            'prof':forms.Textarea(
                attrs={'rows': 10, 'cols': 30,}
            ),
>>>>>>> cf12ca6 (at my mac)
        }