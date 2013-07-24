import urllib

from django.shortcuts import render
from django.http import HttpResponseRedirect

from plugins.opensubtitles import getMovies, getSubtitles, getLink
from plugins.piratebay import getTorrents


def index(request):

	q = request.POST.get('q')

	if request.method == 'POST' and q != '':

		query = __toQuote(request.POST.get('q'))
		movies = getMovies(query)

		if movies:

			movie = movies[0] 
			torrents = getTorrents(__toQuote(movie['name']))

			link = __subtitle(torrents[0][1], 'pob', movie['id'])
			torrents[0].append(link)
			link = __subtitle(torrents[0][1], 'eng', movie['id'])
			torrents[0].append(link)

			link = __subtitle(torrents[1][1], 'pob', movie['id'])
			torrents[1].append(link)
			link = __subtitle(torrents[1][1], 'eng', movie['id'])
			torrents[1].append(link)

			return render(request, 'main/index.html', {'torrents': torrents, 'total': len(torrents), 'q': request.POST.get('q')})
		else:
			return render(request, 'main/index.html', {'total': 0, 'q': request.POST.get('q')})

	return render(request, 'main/index.html')


def __subtitle(torrentTitle, language, movieId):
	subtitles = getSubtitles(language, movieId)
	link = getLink(torrentTitle, subtitles)
	return link


def __toQuote(text):
	return urllib.quote(text)	


def about(request):
	return render(request, 'main/about.html')


def custom_404(request):
	return render(request, '404.html', {}, status=404)


def custom_500(request):
	return render(request, '500.html', {}, status=500)

