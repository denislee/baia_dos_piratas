import requests
import re

from bs4 import BeautifulSoup

PIRATEBAY_URL = 'http://piratebay.se'
SEARCH_PATERN = '/search/%s/0/7/0'
SEARCH_PATERN_MOVIE = '/search/%s/0/7/200'
TABLE_BEGIN = '<table id="searchResult">'
TABLE_END = '</table>'


def getFirstTorrent(query):
	return getTorrents(query)[0]


def getTorrents(query):
	htmlData = requests.get(PIRATEBAY_URL+(SEARCH_PATERN_MOVIE % query)).text
	htmlData = htmlData.replace('\n', '')
	htmlData = htmlData.replace('\r', '')

	tableData = __trimTable(htmlData, TABLE_BEGIN, TABLE_END)
	soup = BeautifulSoup(tableData)
	torrents = __makeList(soup, 3)
	torrents.remove([]) # remove first empty item
	return torrents


def getAllTorrents(query):
	htmlData = requests.get(PIRATEBAY_URL+(SEARCH_PATERN_MOVIE % query)).text
	htmlData = htmlData.replace('\n', '')
	htmlData = htmlData.replace('\r', '')

	tableData = __trimTable(htmlData, TABLE_BEGIN, TABLE_END)
	soup = BeautifulSoup(tableData)
	torrents = __makeList(soup, 100, False)
	torrents.remove([]) # remove first empty item
	return torrents


def __trimTable(htmlData, begin, end):
	tableData = 'not found ):'
	if (htmlData):
		tableData = htmlData[htmlData.find(begin):htmlData.find(end)+len(end)]
	return tableData


def __makeList(table, limit=100, shortName=True):
	result = []
	allrows = table.findAll('tr', limit=limit)
	for row in allrows:
		result.append([])
		allcols = row.findAll('td')
		for col in allcols:
			thestrings = [unicode(s) for s in col.findAll(text=True)]
			thetext = ''.join(thestrings)

			regex = re.compile(r'[\n\r\t]')
			thestrings = regex.sub('', str(thestrings))

			# getting only torrent title
			if thetext.find('Uploaded') > 0 and shortName:
				result[-1].append(thetext[:thetext.find('Uploaded')])
			else:
				result[-1].append(thetext)

			# link to details
			urlTag = col.find('a', 'detLink')
			if urlTag:
				url = PIRATEBAY_URL+urlTag.get('href')
				result[-1].append(url)

			# link to torrent
			urlTag = col.find('a', title='Download this torrent using magnet')
			if urlTag:
				url = urlTag.get('href')
				result[-1].append(url)

	return result

