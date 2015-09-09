from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	followers = models.ManyToManyField('self', related_name='followees_test', symmetrical=False)


class Post(models.Model):
	author = models.ForeignKey(User, related_name='posts')
	title = models.CharField(max_length=255)
	body = models.TextField(blank=True, null=True)


class Photo(models.Model):
	post = models.ForeignKey(Post, related_name='photos')
	image = models.ImageField(upload_to="static/images/test/%Y/%m/%d")
