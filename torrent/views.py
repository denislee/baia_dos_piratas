import urllib

from django.shortcuts import render
from django.http import HttpResponseRedirect

from plugins.piratebay import getAllTorrents


def index(request):

	q = request.POST.get('q')
	if (q and request.method == 'POST'):
		query = __toQuote(q)
		torrents = getAllTorrents(query)
		return render(request, 'torrent/index.html', {'torrents': torrents, 'total': len(torrents), 'q': query})
	elif (q):
		return render(request, 'torrent/index.html', {'total': 0, 'q': request.POST.get('q')})

	return render(request, 'torrent/index.html')


def __toQuote(text):
	return urllib.quote(text)	

