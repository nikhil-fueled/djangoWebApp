from tastypie.resources import ModelResource
from django.conf.urls import patterns, include, url
from blog.models import *
from django.contrib.auth.models import User
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS


class UserResource(ModelResource):

	class Meta:
		queryset=User.objects.all()
		resource_name='auth/user'
		authentication=Authentication()
		authorization=Authorization()


class PostResource(ModelResource):
	#comment=fields.ToManyField('blog.api.resources.CommentResource', 'comments', full=True, null=True)
	user=fields.ForeignKey(UserResource, 'user')
	class Meta:
		queryset=Post.objects.all()
		resource_name='post'
		authentication=Authentication()
		authorization = Authorization()
		filtering={'title':ALL}


class CommentResource(ModelResource):
	post=fields.ForeignKey(PostResource,'post')
	user=fields.ForeignKey(UserResource, 'user')
	class Meta:
		queryset=Comment.objects.all()
		authentication=Authentication()
		resource_name='comment'
		authorization=Authorization()
		filtering={'post': ALL_WITH_RELATIONS, 

					}

