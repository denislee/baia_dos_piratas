import requests
import json 
import difflib

from django.http import HttpResponse

from bs4 import BeautifulSoup

MAIN_URL = 'http://www.opensubtitles.org'

MOVIE_QUERY = MAIN_URL + '/libs/suggest.php?format=json3&MovieName=%s&SubLanguageID=null'

# pob or eng
SUBTITLES_QUERY = MAIN_URL + '/en/search/sublanguageid-%s/idmovie-%s'
SUBTITLE_DOWNLOAD = MAIN_URL + '/en/subtitleserve/sub/%s'

TABLE_BEGIN = '<table id="search_results">'
TABLE_END = '<legend>Download at 25 MBit</legend>'

TR_CLASS_PATTERN = 'change odd expandable'


def guestMovie(query, movieList):
	movies = difflib.get_close_matches(query, movieList)
	getMovies(query)
	return movie


def getMovies(query):
	movies = requests.get(MOVIE_QUERY % query).text
	if movies:
		data = json.loads(movies)
	else:
		data = ''
	return data 


# webService sugestion for movies / returns json
def s(request):
	q = request.GET.get('q')
	if request.method == 'GET' and q != '':
		# movies = 'suggestCallBack(%s)' % requests.get(MOVIE_QUERY % q).text
		movies = requests.get(MOVIE_QUERY % q).text
		if movies:
			jsonp = '{"movies":%s}' % movies
		else:
			jsonp = ''
	else:
		jsonp = ''
	return HttpResponse(jsonp, content_type='application/json')


def getSubtitles(language, idMovie):
	htmlData = requests.get(SUBTITLES_QUERY % (language, idMovie)).text
	tableData = __trimTable(htmlData, TABLE_BEGIN, TABLE_END)
	soup = BeautifulSoup(tableData)
	subtitles = __makeList(soup)
	response = subtitles 
	return response


def getLink(torrentTitle, subtitles):
	titles = __onlyTitles(subtitles) # getting titles
	if (len(difflib.get_close_matches(torrentTitle, titles))):
		choosenOne = difflib.get_close_matches(torrentTitle, titles)[0] # getting the most similar title
		subtitleIndex = titles.index(choosenOne) # index to get full subtitle lists
		movieCode = subtitles[ subtitleIndex ][0] # movie code to construct link
		link = SUBTITLE_DOWNLOAD % movieCode # finally, link (:
	else:
		link = ''
	return link


def __trimTable(htmlData, begin, end):
	tableData = 'not found ):'
	if (htmlData):
		firstPos= htmlData.find(begin)
		tableData = htmlData[firstPos:htmlData.find(end, firstPos)+len(end)]
	return tableData


def __makeList(table):
	subtitles = []
	allrows = table.findAll('tr', TR_CLASS_PATTERN)
	for row in allrows:
		subtitles.append([row.get('id').replace('name', '')])
		subtitles[-1].append(SUBTITLE_DOWNLOAD % row.get('id').replace('name', ''))
		allcols = row.findAll('td')
		for col in allcols:
			thestrings = [unicode(s) for s in col.findAll(text=True)]
			thetext = ''.join(thestrings)
			thetext = thetext.replace('Download at 25 MBitDownload Subtitles Searcher', '')
			thetext = thetext.strip()

			title = col.find('span')
			if bool(title):
				subtitles[-1].append(title.get('title'))
			else:
				title = col.find('a')
				if bool(thetext) or thetext != '' or thetext == 'None':
					subtitles[-1].append(thetext)
				else:
					subtitles[-1].append('-')
			urlTag = col.find('a', 'bnone')
			if urlTag:
				url = MAIN_URL+urlTag.get('href')
				subtitles[-1].append(url)
	return subtitles 


def __onlyTitles(list):
	titles = []
	for item in list:
		titles.append(item[2])
	return titles

