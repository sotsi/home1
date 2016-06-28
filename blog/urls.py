from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^$', views.post_list, name='post_list'),
	url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
	#url(r'^quest/(?P<pk>\d+)/$', views.quest_detail, name='quest_detail'),
	url(r'^post/new/$', views.post_new, name='post_new'),
	url(r'^quest/new/$', views.quest_new, name='quest_new'),
	url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
	url(r'^quest/new/$', views.quest_edit1, name='quest_edit1'),
]