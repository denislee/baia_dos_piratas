import requests
import re

from bs4 import BeautifulSoup

PIRATEBAY_URL = 'http://piratebay.se'
# SEARCH_PATERN = '/search/%s/0/7/0' // generic search
SEARCH_PATERN = '/search/%s/0/7/200'
TABLE_BEGIN = '<table id="searchResult">'
TABLE_END = '</table>'


def getFirstTorrent(query):
	return getTorrents(query)[0]


def getTorrents(query):
	htmlData = requests.get(PIRATEBAY_URL+SEARCH_PATERN.replace('%s',query)).text
	htmlData = htmlData.replace('\n', '')
	htmlData = htmlData.replace('\r', '')

	tableData = trimTable(htmlData, TABLE_BEGIN, TABLE_END)
	soup = BeautifulSoup(tableData)
	torrents = makeList(soup)
	torrents.remove([]) # remove first empty item
	return torrents


def trimTable(htmlData, begin, end):
	tableData = 'not found ):'
	if (htmlData):
		tableData = htmlData[htmlData.find(begin):htmlData.find(end)+len(end)]
	return tableData


def makeList(table):
	result = []
	allrows = table.findAll('tr', limit=3)
	for row in allrows:
		result.append([])
		allcols = row.findAll('td')
		for col in allcols:
			thestrings = [unicode(s) for s in col.findAll(text=True)]
			thetext = ''.join(thestrings)

			regex = re.compile(r'[\n\r\t]')
			thestrings = regex.sub('', str(thestrings))

			# getting only torrent title
			if thetext.find('Uploaded') > 0:
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

