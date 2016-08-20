from django.db import models

from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile

import feedparser
import datetime
from django import forms




class Feed(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    is_active = models.BooleanField(default=False)
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='my_profile')

    def __str__(self):
        return self.title

class Article(models.Model):
    feed = models.ForeignKey(Feed)
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(max_length=200)
    publication_date = models.DateTimeField()
    thumbnail_url = models.URLField(default='http://pbs.twimg.com/profile_images/555400719478444032/ky9g4wh6.png')

    def __str__(self):
        return self.title

class FeedForm(forms.ModelForm):
    class Meta:
        model = Feed
        fields = ('url',)

class MyProfile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='my_profile')
    favourite_snack = models.CharField(_('favourite snack'),
                                       max_length=5)

    feed_url = models.CharField(_('Enter RSS feed URL'),
                                       max_length=200,
                                       default='http://www.singularityhub.com/feed/')


    # feed_content = models.OneToOneField(_('Enter nothing here'),
    #                                    max_length=2000)

    def get_feed(self):
        form = FeedForm(self.feed_url)
        if form.is_valid():
            feed = form.save(commit=False)

            existingFeed = Feed.objects.filter(url = feed.url)
            if len(existingFeed) == 0:

                feedData = feedparser.parse(feed.url)

                feed.title = feedData.feed.title
                feed.save()

                for entry in feedData.entries:
                    article = Article()
                    article.title = entry.title
                    article.url = entry.link
                    article.description = entry.description

                    if 'media_thumbnail' in entry:
                        article.thumbnail_url = entry.media_thumbnail[0]['url']

                    if 'media_content' in entry:
                        article.thumbnail_url = entry.media_content[0]['url']

                    d = datetime.datetime(*(entry.published_parsed[0:6]))
                    dateString = d.strftime('%Y-%m-%d %H:%M:%S')

                    article.publication_date = dateString
                    article.feed = feed
                    article.save()
        return feed.objects.all()



#
#
# # from django.shortcuts import render
# # from .models import Article, Feed
# # from .forms import FeedForm
# # from django.shortcuts import redirect
#
#
# # Create your views here.
#
#
# def articles_list(request):
#     articles = Article.objects.all()
#
#     rows = [articles[x:x+3] for x in range(0, len(articles), 3)]
#
#     t_args = {
#         'articles': articles
#     }
#     return render(request, 'news/articles_list.html', {'rows': rows})
#
#
# def feeds_list(request):
#     feeds = Feed.objects.all
#     return render(request, 'news/feeds_list.html', {'feeds': feeds})
#
#
# def new_feed(request):
#     if request.method == "POST":
#         form = FeedForm(request.POST)
#         if form.is_valid():
#             feed = form.save(commit=False)
#
#             existingFeed = Feed.objects.filter(url = feed.url)
#             if len(existingFeed) == 0:
#
#                 feedData = feedparser.parse(feed.url)
#
#                 feed.title = feedData.feed.title
#                 feed.save()
#
#                 for entry in feedData.entries:
#                     article = Article()
#                     article.title = entry.title
#                     article.url = entry.link
#                     article.description = entry.description
#
#                     if 'media_thumbnail' in entry:
#                         article.thumbnail_url = entry.media_thumbnail[0]['url']
#
#                     if 'media_content' in entry:
#                         article.thumbnail_url = entry.media_content[0]['url']
#
#                     d = datetime.datetime(*(entry.published_parsed[0:6]))
#                     dateString = d.strftime('%Y-%m-%d %H:%M:%S')
#
#                     article.publication_date = dateString
#                     article.feed = feed
#                     article.save()
#
#                 return redirect(feeds_list)
#
#     else:
#         form = FeedForm()
#     return render(request, 'news/new_feed.html', {'form': form})
