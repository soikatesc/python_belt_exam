from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.index),
	url(r'^createUser$',views.createUser),
	url(r'^login$',views.login),
	url(r'^logout$',views.logout),
	url(r'^friends$',views.friends),
	url(r'^addFriend/(?P<friendid>\d+)$',views.addFriend),
	url(r'^removeFriend/(?P<friendid>\d+)$',views.removeFriend),
	url(r'^userprofile/(?P<userid>\d+)$',views.userprofile)
]
