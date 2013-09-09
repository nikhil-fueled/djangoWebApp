from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Tag(models.Model):
	name=models.CharField(max_length=20, unique=True)
	def __unicode__(self):
		return self.name

class Post(models.Model):
	user=models.ForeignKey(User)
	title=models.CharField(max_length=60, unique=True)
	body=models.TextField()
	created=models.DateTimeField(auto_now_add=True)
	tags=models.ManyToManyField(Tag)
	def __unicode__(self):
		return self.title

class Comment(models.Model):
	user=models.ForeignKey(User)
	post= models.ForeignKey(Post, related_name="post")
	body= models.CharField(max_length=200)
	name= models.CharField(max_length=30)
	def __unicode__(self):
		return self.body + " Posted by " + str(self.user)

