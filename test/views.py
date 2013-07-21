import urllib
import requests
import time 

from bs4 import BeautifulSoup

from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.timezone import utc

from plugins.opensubtitles import getFirstMovie 
from plugins.opensubtitles import getSubtitles 

# URL_MOVIES = 'http://www.opensubtitles.org/libs/suggest.php'
# LANGUAGE = 'pob'
# MOVIE_QUERY = MAIN_URL + 'libs/suggest.php?format=json3&MovieName=%s&SubLanguageID=null'
# SUBTITLES_QUERY = MAIN_URL + 'en/search2?MovieName=%s&id=8&action=search&SubLanguageID=pob&SubLanguageID=pob&Season=&Episode=&SubSumCD=&Genre=&MovieByteSize=&MovieLanguage=&MovieImdbRatingSign=1&MovieImdbRating=&MovieCountry=&MovieYearSign=1&MovieYear=&MovieFPS=&SubFormat=&SubAddDate=&Uploader=&IDUser=&IMDBID=&IDMovie=%s&MovieHash='

MAIN_URL = 'http://www.opensubtitles.org/'
SUBTITLES_QUERY = MAIN_URL + 'en/search/sublanguageid-pob/idmovie-%s'
TABLE_BEGIN = '<table id="search_result">'
TABLE_END = '</table>'


def index(request):
	if request.method == 'POST' and request.POST.get('q') != '':
		query = urllib.quote( request.POST.get('q') )

		movie = getFirstMovie(query)

		response = getSubtitles(movie['id'])

		# json = queryMovieSimple(query)
		# print 'json : ' + json
		# host = str(HttpRequest.get_host())
		# print 'objeto py: ' + json.json()

		return render(request, 'test/index.html', { 'json': response })
	return render(request, 'test/index.html')



# def queryMovieSimple(query):
	# json = requests.get(MOVIE_QUERY % urllib.quote( query )).text
	# json = requests.get( \
	# 	'http://www.opensubtitles.org/libs/suggest.php?format=json3&MovieName=' \
	# 	+ urllib.quote( query ) + \
	# 	'&SubLanguageID=null').text
	# return json

# def getCookies(url):
# 	response = requests.get(url)
# 	cookies = response.cookies
# 	print 'getCookies cookie : '+ str(response.cookies)
# 	print 'getCookies header : '+ str(response.headers)
# 	return cookies 

# def queryMovies(movie, cookies):
# 	payload = { \
# 		'format': 'json3', \
# 		'movieName': urllib.quote( movie ), \
# 		'SubLanguageID': OPENSUBTITLES_LANGUAGE, }
# 	headers = { \
# 		'X-Requested-With': 'XMLHttpRequest', \
# 		'Accept': 'application/json, text/javascript, */*; q=0.01', \
# 		'Accept-Encoding': 'gzip,deflate,sdch', \
# 		'Accept-Language': 'en-US,en;q=0.8', \
# 		'Connection': 'keep-alive', \
# 		'Host': 'www.opensubtitles.org', \
# 		'Referer': 'http://www.opensubtitles.org/en', \
# 		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36', } 
# 	return cookies
