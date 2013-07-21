import urllib
import requests
import difflib

from django.shortcuts import render
from django.http import HttpResponseRedirect

from plugins.opensubtitles import getFirstMovie
from plugins.piratebay import getTorrents


def index(request):

	q = request.POST.get('q')

	if request.method == 'POST' and q != '':
		query = toQuote( request.POST.get('q') )

		print '--- opensubtitles ---'
		print 'query: ' + q
		movie = getFirstMovie(query)
		print 'selected movie: ' + str(movie['name'])

		print '--- piratebay ---'
		print 'query: ' + movie['name'] 
		torrents = getTorrents(toQuote(movie['name']))
		#print 'torrents: ' + str(torrents)
		print 'torrent 1: ' + str(torrents[0])
		print 'torrent 2: ' + str(torrents[1])

		print '--- opensubtitles ---'
		# request subtitles

		# difflib.get_close_matches('Hello', subtitles)

		return render(request, 'main/index.html', {'torrents': torrents, 'total': len(torrents), 'q': request.POST.get('q')})
	return render(request, 'main/index.html')


def toQuote(text):
	return urllib.quote(text)	


def about(request):
	return render(request, 'main/about.html')


def custom_404(request):
	return render(request, '404.html', {}, status=404)


def custom_500(request):
	return render(request, '500.html', {}, status=500)

