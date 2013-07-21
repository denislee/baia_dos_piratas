from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^about/$', 'main.views.about', name='about'),
	url(r'^test/$', 'test.views.index', name='test'),
	url(r'^$', 'main.views.index', name='main'),
)

handler404 = 'main.views.custom_404'
handler500 = 'main.views.custom_500'