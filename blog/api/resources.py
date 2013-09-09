from tastypie.resources import ModelResource, Resource
from django.conf.urls import patterns, include, url
from blog.models import *
from django.contrib.auth.models import User
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
from django.core.paginator import Paginator

class UserResource(ModelResource):

	class Meta:
		queryset=User.objects.all()
		resource_name='user'
		authentication=Authentication()
		authorization=Authorization()

class PostResource(ModelResource):
	comment=fields.ToManyField('blog.api.resources.CommentResource', ''	, full=True, null=True)
	user=fields.ForeignKey(UserResource, 'user')
	tags=fields.ToManyField('blog.api.resources.TagResource', 'tags', full=True)
	class Meta:
		queryset=Post.objects.all()
		resource_name='post'
		authentication=Authentication()
		authorization = Authorization()
		filtering={'title':ALL}
	def dehydrate(self, bundle):
		obj=Post.objects.get(id=bundle.data['id'])
		comment_list= Comment.objects.filter(post=obj)
	 	comments=[]
		for comment in comment_list:
			comments.append(comment)
		bundle.data['comment']=comments
		return bundle
	def save_m2m(self, bundle):
		for field_name, field_object in self.fields.items():
			if not getattr(field_object, 'is_m2m', False):
				continue

			if not field_object.attribute:
				continue

			if field_object.readonly:
				continue

			related_mngr=getattr(bundle.obj,field_object.attribute)

			related_objs=[]
			for related_bundle in bundle.data[field_name]:
				try:
					tag=Tag.objects.get(name=related_bundle.obj.name)

				except Tag.DoesNotExist:
					tag=related_object.obj
					tag.save()

				related_objs.append(tag)
			related_mngr.add(*related_objs)


class CommentResource(ModelResource):
	post=fields.ForeignKey(PostResource,'post')
	user=fields.ForeignKey(UserResource, 'user')
	class Meta:
		queryset=Comment.objects.all()
		authentication=Authentication()
		resource_name='comment'
		authorization=Authorization()
		filtering={'post': ALL_WITH_RELATIONS}

class PostComment():
	def __init__ (self, post, comments):
		self.post=post
		self.comments=comments
		

	

class PostCommentResource(Resource):
	post=fields.CharField(attribute='post')
	#comments=fields.ToManyField(CommentResource,attribute='comments')
	comments=fields.CharField(attribute='comments')
	class Meta:
		resource_name='postcomment'
		object_class=Post
		authentication=Authentication()
		authorization=Authorization()
	def _bucket(self):
		client=self._client
	def obj_get_list(self, request=None, **kwargs):
		posts=[]

	def obj_get(self, request=None, **kwargs):
		pk=kwargs['pk']
		#bucket= self._bucket()
		message=kwargs['pk']
		message=Post.objects.get(pk=message)
		comments= Comment.objects.filter(post=message)
		cm=[]
		for comment in comments:
			cm.append(comment.body)
		p=PostComment(post=message.title, comments=cm)
		#p=PostComment(post="abcd", comments="sdfsdfsd")
		return p

class TagResource(ModelResource):
	post= fields.ToManyField(PostResource,'post_set',)
	class Meta:
		queryset=Tag.objects.all()
		authentication=Authentication()
		authorization=Authorization()

class SearchResource(ModelResource):
	class Meta:
		authorization=Authorization()
		authentication=Authentication()
	def prepend_urls(self):
		return[url(r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),]
	def get_search(self, request, **kwargs):
		reqdata=request.GET.get('q','')
		results=[]
		posttitle=Post.objects.filter(title__contains=reqdata)
		postbody=Post.objects.filter(body__contains=reqdata)
		tag=Tag.objects.filter(name__contains=reqdata)
		posttag= Post.objects.filter(tags=tag)
		results.append({'posttitle':posttitle})
		results.append({'postbody':postbody})
		results.append({'tag':posttag})
		'''objects=[]
		for data in results:
			for obj in data:
				bundle=self.build_bundle(obj=obj, request=request)
				bundle=self.full_dehydrate(bundle)
				objects.append(bundle)
		object_list={
			'objects':objects,
		}
		'''


		return self.create_response(request, results)



