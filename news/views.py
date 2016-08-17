from django.shortcuts import render
from .models import Article

# Create your views here.


def articles_list(request):
    articles = Article.objects.all

    t_args = {
        'articles': articles
    }
    return render(request, 'news/articles_list.html', {'articles': articles})
