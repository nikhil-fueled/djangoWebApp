from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^addComment/$', views.addComment, name="addComment"),
    url(r'^view/(?P<pk>\d+)$', views.view, name="view"),
 	url(r'^login$', views.login, name="login"),
 	url(r'^logout$', views.logout, name="logout"),
)