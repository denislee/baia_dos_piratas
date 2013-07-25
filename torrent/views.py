import urllib

from django.shortcuts import render

from plugins.piratebay import getAllTorrents


def index(request):
	q = request.POST.get('q')
	if (q and request.method == 'POST'):
		query = __toQuote(q)
		torrents = getAllTorrents(query)
		return render(request, 'torrent/index.html', {'torrents': torrents, 'total': len(torrents), 'q': q})
	elif (q):
		return render(request, 'torrent/index.html', {'total': 0, 'q': q})
	return render(request, 'torrent/index.html')


def __toQuote(text):
	return urllib.quote(text.encode('utf8'))	

