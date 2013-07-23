import urllib
import requests
import difflib

from django.shortcuts import render
from django.http import HttpResponseRedirect

from plugins.opensubtitles import getMovies, getSubtitles, getLink
from plugins.piratebay import getTorrents


def index(request):

	q = request.POST.get('q')

	if request.method == 'POST' and q != '':

		query = toQuote( request.POST.get('q') )
		movies = getMovies(query)

		if movies:

			movie = movies[0] 
			torrents = getTorrents(toQuote(movie['name']))

			link = subtitle(torrents[0][1], movie['id'])
			torrents[0].append(link)

			link = subtitle(torrents[1][1], movie['id'])
			torrents[1].append(link)

			return render(request, 'main/index.html', {'torrents': torrents, 'total': len(torrents), 'q': request.POST.get('q')})
		else:
			return render(request, 'main/index.html', {'total': 0, 'q': request.POST.get('q')})

	return render(request, 'main/index.html')


def subtitle(torrentTitle, movieId):
	subtitles = getSubtitles(movieId)
	link = getLink(torrentTitle, subtitles)
	return link


def toQuote(text):
	return urllib.quote(text)	


def about(request):
	return render(request, 'main/about.html')


def custom_404(request):
	return render(request, '404.html', {}, status=404)


def custom_500(request):
	return render(request, '500.html', {}, status=500)

