from statistics import mode
from django.core.validators import ProhibitNullCharactersValidator
from django.db import models
from django.db.models.deletion import CASCADE

class Post(models.Model):
	owner = models.ForeignKey('accounts.User', verbose_name='オーナー', on_delete=models.CASCADE, related_name='photo_owner')
	photo = models.ImageField(upload_to='images/',verbose_name='photo')
	comment = models.TextField(max_length=300, blank=True)
	pub_date = models.DateTimeField(auto_now_add=True)
	meow_count = models.IntegerField(default=0)
	detail = models.BooleanField(default=False,verbose_name="里親募集")
	gender = models.BooleanField(default=True, blank=True)
	age = models.CharField(max_length=30, blank=True)
	kind = models.CharField(max_length=30, blank=True)
	class Meta:
		db_table = 'posts'
		ordering = ('-pub_date',)

class Gallery(models.Model):
   # Imageのオーナーを設定する
   owner = models.ForeignKey('accounts.User', verbose_name='オーナー', on_delete=models.CASCADE)
   pub_date = models.DateTimeField(auto_now_add=True)
   photo = models.ImageField(upload_to='gallery/')
   
   class Meta:
       db_table = 'gallery'
   def __str__(self):
       return str(self.pk)

#未使用クラス
class Profile(models.Model):
	owner = models.ForeignKey('accounts.User', related_name='pfofile_owner', on_delete=models.CASCADE)
	avatar = models.ImageField(upload_to='avatar/', verbose_name="アイコン画像",blank=True, null=True)  
	prof = models.CharField(max_length=300, blank=True, null=True, verbose_name='自己紹介')
	sato_oya = models.BooleanField(blank=False)


	class Meta:
		db_table = 'profiles'
	def __str__(self):
		return str(self.pk)

# related_nameは、他クラスから逆参照するときにどのような名前で参照するかを指定しています。
class SubComment(models.Model):
	owner = models.ForeignKey('accounts.User', related_name='subcomment_owner', on_delete=models.CASCADE)
	target = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='target_post')
	text = models.TextField(max_length=200,verbose_name='comment')
	pub_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'SubComment'
		ordering = ('-pub_date',)
	def __str__(self):
		return self.text