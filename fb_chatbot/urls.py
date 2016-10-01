from django.conf.urls import patterns,url
from fb_chatbot import views
from .views import BotView


urlpatterns = patterns('',
	url(r'^$', views.index,name = 'index'),
	url(r'^facebook_auth/?$', BotView.as_view()))