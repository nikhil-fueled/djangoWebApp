from django.db import models

# Create your models here.
class Post(models.Model):
	title=models.CharField(max_length=60)
	body=models.TextField()
	created=models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return self.title

class Comment(models.Model):
	post= models.ForeignKey(Post)
	body= models.CharField(max_length=200)
	name= models.CharField(max_length=30)

