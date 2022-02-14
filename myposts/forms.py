from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import Post, Profile,SubComment

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
        }

class CommentForm(forms.ModelForm):
    # body=forms.CharField(widget=forms.Textarea(attrs={'class':'input ismedium'}),required=True)

    class Meta:
        model = SubComment
        exclude = ('owner','target', 'pub_date')
        fields = (
            'text',
        )
        widgets = {
            'comment': forms.Textarea(
               attrs={'rows': 5, 'cols': 30}
            ),
        }