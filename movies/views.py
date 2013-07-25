import urllib

from django.shortcuts import render
from django.http import HttpResponseRedirect

from plugins.opensubtitles import getSubtitles, getLink
from plugins.piratebay import getTorrents


def index(request):

	query = request.GET.get('q')
	movieId = request.GET.get('movieId')

	# print 'query '+ str(query)
	# print 'movieId '+ str(movieId)

	if (query and movieId):

		torrents = getTorrents(query)

		link = __subtitle(torrents[0][1], 'pob', movieId)
		torrents[0].append(link)
		link = __subtitle(torrents[0][1], 'eng', movieId)
		torrents[0].append(link)

		link = __subtitle(torrents[1][1], 'pob', movieId)
		torrents[1].append(link)
		link = __subtitle(torrents[1][1], 'eng', movieId)
		torrents[1].append(link)

		return render(request, 'movies/index.html', {'torrents': torrents, 'total': len(torrents), 'q': query})

	return render(request, 'movies/index.html')


def __subtitle(torrentTitle, language, movieId):
	subtitles = getSubtitles(language, movieId)
	link = getLink(torrentTitle, subtitles)
	return link


def __toQuote(text):
	return urllib.quote(text)	

