import datetime
import os
import sys
import urllib2
# import requests

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.timezone import utc
# from django.contrib.auth.decorators import login_required

# from stories.models import Story
# from stories.forms import StoryForm

PIRATEBAY_URL = 'http://piratebay.se'

def index(request):
	if request.method == 'POST':
		if request.POST.get('q') == '':
			return HttpResponseRedirect('/')
		response = urllib2.urlopen(PIRATEBAY_URL)
		# response = requests.get(PIRATEBAY_URL)
		return render(request, 'main/index.html', {'response': response.read() })
	else:
		return render(request, 'main/index.html')

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
