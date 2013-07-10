from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^about/', 'main.views.about', name='about'),
	url(r'^legendas/', 'opensubtitles.views.index', name='opensubtitles'),
	url(r'', 'main.views.index', name='main'),
)
