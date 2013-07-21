
import requests
import json 

from bs4 import BeautifulSoup

MAIN_URL = 'http://www.opensubtitles.org/'

MOVIE_QUERY = MAIN_URL + 'libs/suggest.php?format=json3&MovieName=%s&SubLanguageID=null'
SUBTITLES_QUERY = MAIN_URL + 'en/search/sublanguageid-pob/idmovie-%s'

TABLE_BEGIN = '<table id="search_results">'
TABLE_END = '</table>'


def getFirstMovie(query):
	return getMovies(query)[0]


def getMovies(query):
	movies = requests.get(MOVIE_QUERY % query).text
	data = json.loads(movies)
	return data 


def getSubtitles(idMovie):
	htmlData = requests.get(SUBTITLES_QUERY % idMovie).text

	print '--html find --'
	print htmlData.find(TABLE_BEGIN)

	tableData = trimTable(htmlData, TABLE_BEGIN, TABLE_END)

	print '--table--'
	print str(tableData) 

	soup = BeautifulSoup(tableData)
	subtitles = makeList(soup)
	response = subtitles 
	return response


def trimTable(htmlData, begin, end):
	tableData = 'not found ):'
	if (htmlData):
		firstPos= htmlData.find(begin)
		tableData = htmlData[firstPos:htmlData.find(end, firstPos)+len(end)]
	return tableData


def makeList(table):
	result = []
	# allrows = table.findAll('tr', limit=3)
	allrows = table.findAll('tr')
	for row in allrows:
		result.append([])
		allcols = row.findAll('td')
		for col in allcols:
			thestrings = [unicode(s) for s in col.findAll(text=True)]
			thetext = ''.join(thestrings)
			result[-1].append(thetext)
			# print 'col' + str(col)
			urlTag = col.find('a', 'detLink')
			if urlTag:
				url = PIRATEBAY_URL+urlTag.get('href')
				result[-1].append(url)
			urlTag = col.find('a', title='Download this torrent using magnet')
			if urlTag:
				url = urlTag.get('href')
				result[-1].append(url)
				
	return result

