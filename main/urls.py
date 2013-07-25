from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

	# only for movies
	url(r'^m/$', 'movies.views.index', name='movies'),
	url(r'^s/$', 'plugins.opensubtitles.s', name='suggestions'),

	# test
	# url(r'^test/$', 'test.views.index', name='test'),

	# generic torrent search
	url(r'^about/$', 'main.views.about', name='about'),
	url(r'^$', 'torrent.views.index', name='main'),
)


handler404 = 'main.views.custom_404'
handler500 = 'main.views.custom_500'