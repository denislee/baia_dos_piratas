import urllib
import requests
import difflib

from django.shortcuts import render
from django.http import HttpResponseRedirect

from plugins.opensubtitles import getFirstMovie, getSubtitles, getLink
from plugins.piratebay import getTorrents


def index(request):

	q = request.POST.get('q')

	if request.method == 'POST' and q != '':
		query = toQuote( request.POST.get('q') )

		# print '--- opensubtitles ---'
		# print 'query: ' + q
		movie = getFirstMovie(query)
		# print 'selected movie: ' + str(movie['name'])
		# print 'movie id: ' + str(movie['id'])

		# print '--- piratebay ---'
		# print 'query: ' + movie['name'] 
		torrents = getTorrents(toQuote(movie['name']))
		# print 'torent 1 name: ' + torrents[0][1]
		# print 'torent 2 name: ' + torrents[1][1]

		# print 'torent 1 numb: ' + str( torrents[0][1].find('Uploaded') )
		# print 'torent 2 numb: ' + str( torrents[1][1].find('Uploaded') )

		# # checking again
		# if torrents[0][1].find('Uploaded') > 0:
		# 	newTitle = torrents[0][1]
		# 	torrents[0][1] = newTitle[:newTitle.find('Uploaded')]

		# if torrents[1][1].find('Uploaded') > 0:
		# 	newTitle = torrents[1][1]
		# 	torrents[1][1] = newTitle[:newTitle.find('Uploaded')]

		link = subtitle(torrents[0][1], movie['id'])
		torrents[0].append(link)

		link = subtitle(torrents[1][1], movie['id'])
		torrents[1].append(link)

		# print 'torrent 1 link: ' + str(torrents[0][6])
		# print 'torrent 2 link: ' + str(torrents[1][6])

		# print 'torrent 1: ' + str(torrents[0])
		# print 'torrent 2: ' + str(torrents[1])

		# print '--- opensubtitles ---'
		# request subtitles

		# difflib.get_close_matches('Hello', subtitles)

		return render(request, 'main/index.html', {'torrents': torrents, 'total': len(torrents), 'q': request.POST.get('q')})
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

