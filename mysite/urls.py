from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from tastypie.api import Api
from blog.api.resources import PostResource, CommentResource, UserResource, PostCommentResource, TagResource, SearchResource
from django.contrib import admin

admin.autodiscover()


v1_api=Api(api_name='v1')
v1_api.register(PostResource())
v1_api.register(CommentResource())
v1_api.register(UserResource())
v1_api.register(PostCommentResource())
v1_api.register(TagResource())
v1_api.register(SearchResource())
urlpatterns = patterns('',
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls', namespace="blog")),
    url(r'^api/', include(v1_api.urls)),
)