from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^addComment/$', views.addComment, name="addComment"),
    url(r'^view/(?P<pk>\d+)$', views.view, name="view"),
)