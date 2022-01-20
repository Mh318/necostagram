# Generated by Django 3.0.4 on 2022-01-07 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myposts', '0006_remove_profile_kind'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='profile',
            name='prof',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='自己紹介'),
        ),
    ]
