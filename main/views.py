import urllib
import requests
import time 

from bs4 import BeautifulSoup

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.timezone import utc

PIRATEBAY_URL = 'http://piratebay.se'
SEARCH_PATERN = '/search/%s/0/7/0'

def about(request):
	return render(request, 'main/about.html')
	
def index(request):
	if request.method == 'POST':
		startApp = time.clock()
		if request.POST.get('q') == '':
			return HttpResponseRedirect('/')	
		query = urllib.quote( request.POST.get('q') )
		htmlData = requests.get(PIRATEBAY_URL+SEARCH_PATERN.replace('%s',query)).text
		tableData = trimTable(htmlData)
		soup = BeautifulSoup(tableData)
		torrents = makeList(soup)
		stopApp = time.clock()
		print '[performance-APP] ' + str(stopApp - startApp)
		return render(request, 'main/index.html', {'torrents': torrents, 'q': request.POST.get('q')})
	else:
		return render(request, 'main/index.html')


def trimTable(htmlData):
	begin = '<table id="searchResult">'
	end = '</table>' 
	start = time.clock()
	tableData = 'not found ):'
	if (htmlData):
		tableData = htmlData[htmlData.find(begin):htmlData.find(end)+len(end)]
	stop = time.clock()
	print '[performance-trimTable] ' + str(stop - start)
	return tableData


def trimTorrentLink(htmlData):
	begin = 'href="magnet:'
	end = 'Get this torrent">'
	start = time.clock()
	tableData = 'not found ):'
	if (htmlData):
		tableData = htmlData[htmlData.find(begin)+6:htmlData.find(end)-9]
	stop = time.clock()
	print '[performance-trimTorrentLink] ' + str(stop - start)
	return tableData


def makeList(table):
	start = time.clock()
	result = []
	allrows = table.findAll('tr', limit=3)
	for row in allrows:
		result.append([])
		allcols = row.findAll('td')
		for col in allcols:
			thestrings = [unicode(s) for s in col.findAll(text=True)]
			thetext = ''.join(thestrings)
			result[-1].append(thetext)
			print 'col' + str(col)
			urlTag = col.find('a', 'detLink')
			if urlTag:
				url = PIRATEBAY_URL+urlTag.get('href')
				result[-1].append(url)
			urlTag = col.find('a', title='Download this torrent using magnet')
			if urlTag:
				url = urlTag.get('href')
				result[-1].append(url)
	stop = time.clock()
	print '[performance-makeList] ' + str(stop - start)
	return result
