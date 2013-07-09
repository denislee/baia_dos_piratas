import datetime
import urllib
import urllib2
import HTMLParser 

import time 

from bs4 import BeautifulSoup
from urlparse import urlparse

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.timezone import utc
# from django.contrib.auth.decorators import login_required

# from stories.models import Story
# from stories.forms import StoryForm

PIRATEBAY_URL = 'http://piratebay.se'
SEARCH_PATERN = '/search/%s/0/7/0'

def index(request):
	if request.method == 'POST':
		startApp = time.clock()

		query = urllib.quote( request.POST.get('q') )
		if query == '':
			return HttpResponseRedirect('/')
		htmlData = urllib2.urlopen(PIRATEBAY_URL+SEARCH_PATERN.replace('%s',query)).read()

		tableData = trimTable(htmlData)
		soup = BeautifulSoup(tableData)
		torrents = makeList(soup)

		stopApp = time.clock()
		print '[performance-APP] ' + str(stopApp - startApp)

		return render(request, 'main/index.html', {'torrents': torrents})
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
		# -len(end)]

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

			urlTag = col.find('a', 'detLink')
			if urlTag:
				url = urlTag.get('href')
				result[-1].append(url)

			urlTag = col.find('a', title='Download this torrent using magnet')
			if urlTag:
				url = urlTag.get('href')
				result[-1].append(url)			

	stop = time.clock()
	print '[performance-makeList] ' + str(stop - start)

	return result

# def getTorrentLink(url):
# 	torrentURL = 'error'
# 	htmlData = urllib2.urlopen(PIRATEBAY_URL+url).read()
# 	print '[getTorrentLink] ' +PIRATEBAY_URL+url

# 	start = time.clock()

# 	# soup = BeautifulSoup(trimHTML('href="magnet:','Get this torrent">',htmlData))
# 	# print 'get this torrent: ' + trimTorrentLink(htmlData)
# 	# torrentURL = soup.find('a', title='Get this torrent').get('href')

# 	stop = time.clock()
# 	print '[performance-getTorrentLink] ' + str(stop - start)

# 	return trimTorrentLink(htmlData) 

# 	# print '[torrentURL] '+str(torrentURL)


# @login_required
# def story(request):
# 	if request.method == 'POST':
# 		form = StoryForm(request.POST)
# 		if form.is_valid():
# 			story =	form.save(commit=False)
# 			story.moderator = request.user
# 			story.save()
# 			return HttpResponseRedirect('/')
# 	else:
# 		form = StoryForm()
# 	return render(request, 'stories/story.html', {'form': form})

# @login_required
# def vote(request):
# 	story = get_object_or_404(Story, pk=request.POST.get('story')) 
# 	story.points += 1
# 	story.save()
# 	user = request.user
# 	user.liked_stories.add(story)
# 	user.save()
# 	return HttpResponse()
