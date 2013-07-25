# import urllib

from django.shortcuts import render
# from django.http import HttpResponseRedirect

# from plugins.opensubtitles import getMovies, getSubtitles, getLink
# from plugins.piratebay import getTorrents


def about(request):
	return render(request, 'main/about.html')


def custom_404(request):
	return render(request, '404.html', {}, status=404)


def custom_500(request):
	return render(request, '500.html', {}, status=500)


# def index(request):

# 	query = request.GET.get('q')
# 	movieId = request.GET.get('movieId')

# 	print 'query '+ str(query)
# 	print 'movieId '+ str(movieId)

# 	if (query and movieId):

# 		torrents = getTorrents(query)

# 		link = __subtitle(torrents[0][1], 'pob', movieId)
# 		torrents[0].append(link)
# 		link = __subtitle(torrents[0][1], 'eng', movieId)
# 		torrents[0].append(link)

# 		link = __subtitle(torrents[1][1], 'pob', movieId)
# 		torrents[1].append(link)
# 		link = __subtitle(torrents[1][1], 'eng', movieId)
# 		torrents[1].append(link)

# 		return render(request, 'main/index.html', {'torrents': torrents, 'total': len(torrents), 'q': query})
# 		# else:
# 			# return render(request, 'main/index.html', {'total': 0, 'q': request.POST.get('q')})

# 	return render(request, 'main/index.html')



# def test_moviesLayout(request):
# 	return render(request, 'main/moviesLayout.html')



# def __subtitle(torrentTitle, language, movieId):
# 	subtitles = getSubtitles(language, movieId)
# 	link = getLink(torrentTitle, subtitles)
# 	return link


# def __toQuote(text):
# 	return urllib.quote(text)	

