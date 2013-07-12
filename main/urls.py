from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^about/$', 'main.views.about', name='about'),
	url(r'^legendas/$', 'opensubtitles.views.index', name='opensubtitles'),
	url(r'^$', 'main.views.index', name='main'),
)
