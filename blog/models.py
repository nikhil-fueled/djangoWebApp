from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
	user=models.ForeignKey(User)
	title=models.CharField(max_length=60)
	body=models.TextField()
	created=models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return self.title

class Comment(models.Model):
	user=models.ForeignKey(User)
	post= models.ForeignKey(Post, related_name="posts")
	body= models.CharField(max_length=200)
	name= models.CharField(max_length=30)

