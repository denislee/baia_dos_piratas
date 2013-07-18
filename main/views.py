import urllib
import requests
import time 

from bs4 import BeautifulSoup

from django.shortcuts import render
from django.http import HttpResponseRedirect

PIRATEBAY_URL = 'http://piratebay.se'
SEARCH_PATERN = '/search/%s/0/7/0'
TABLE_BEGIN = '<table id="searchResult">'
TABLE_END = '</table>'

def custom_404(request):
	return render(request, '404.html', {}, status=404)


def custom_500(request):
	return render(request, '500.html', {}, status=500)


def about(request):
	return render(request, 'main/about.html')
	

def index(request):
	if request.method == 'POST' and request.POST.get('q') != '':
		query = urllib.quote( request.POST.get('q') )
		htmlData = requests.get(PIRATEBAY_URL+SEARCH_PATERN.replace('%s',query)).text
		tableData = trimTable(htmlData, TABLE_BEGIN, TABLE_END)
		soup = BeautifulSoup(tableData)
		torrents = makeList(soup)
		return render(request, 'main/index.html', {'torrents': torrents, 'total': len(torrents), 'q': request.POST.get('q')})
	return render(request, 'main/index.html')


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
	return result
