from urlparse import urlparse

from django.db import models

# class Torrent(models.Model):
# 	title = models.CharField(max_length=200)
# 	url = models.URLField()
# 	seeders = models.IntegerField(default=0)
# 	leechers = models.IntegerField(default=0)
# 	size = models.CharField(max_length=200)
# 	uploaded_at = models.CharField(max_length=200)

# 	@property
# 	def domain(self):
# 		return urlparse(self.url).netloc

# 	def __unicode__(self):
# 		return self.title	
