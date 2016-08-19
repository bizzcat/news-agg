from django.shortcuts import render
from .models import Article, Feed
from .forms import FeedForm
from django.shortcuts import redirect

import feedparser
import datetime

# Create your views here.


def articles_list(request):
    articles = Article.objects.all()

    rows = [articles[x:x+3] for x in range(0, len(articles), 3)]

    t_args = {
        'articles': articles
    }
    return render(request, 'news/articles_list.html', {'rows': rows})


def feeds_list(request):
    feeds = Feed.objects.all
    return render(request, 'news/feeds_list.html', {'feeds': feeds})


def new_feed(request):
    if request.method == "POST":
        form = FeedForm(request.POST)
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

                    d = datetime.datetime(*(entry.published_parsed[0:6]))
                    dateString = d.strftime('%Y-%m-%d %H:%M:%S')

                    article.publication_date = dateString
                    article.feed = feed
                    article.save()

                return redirect(feeds_list)

    else:
        form = FeedForm()
    return render(request, 'news/new_feed.html', {'form': form})
