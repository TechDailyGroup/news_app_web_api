import json

from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

from main.models import Article
from external_data_access.models import ArticleText
from utils.api_utils import get_json_dict
from account.decorators import login_required

def __get_article_text(article):

    ret = ""
    
    article_elem_list = json.loads(article.content)

    for elem in article_elem_list:
        if elem['type'] == 'text':
            ret = ret + elem['data'] + "\n"

    return ret
    

@login_required
@require_GET
def get_latest_articles(request):
    """
    request: {
      "section": <str>,
      "count": <int>
    }
    response data: {
      "articles": [
        {
          "id": int,
          "title": <str>,
          "text": <str>
          "publish_time": <YYYY-mm-dd HH-MM-ss>
        },
        ...
      ]
    }
    """

    if request.user.username != "TechDailyGroup":
        return HttpResponse("Permission Denied")

    count = int(request.GET['count'])
    count = min(count, 1000)
    articles = Article.objects.filter().order_by('-publish_time')[0:count]

    articles_json_data = []

    for article in articles:
        if not hasattr(article, 'article_text'):
            article_text = ArticleText(article=article, text=__get_article_text(article))
            article_text.save()
        article_dict = {
            'id': article.id,
            'title': article.title,
            'text': article.article_text.text,
            'publish_time': article.publish_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        articles_json_data.append(article_dict)

    json_dict = get_json_dict(data={"articles": articles_json_data})

    return JsonResponse(json_dict)

@login_required
@require_GET
def get_not_indexed_articles(request):
    """
    request: {
      'engine': <str, "es"/"solr">
    }
    response: {
      'articles': [{
        'id': <int>,
        'title': <str>,
        'text': <str>,
        'publish_time': <str>
      }]
    }
    """

    if request.user.username != "TechDailyGroup":
        return HttpResponse("Permission Denied")

    engine =request.GET['engine']

    if engine == "es":
        not_indexed_articles = Article.objects.filter(Q(article_text=None) | Q(article_text__indexed_by_es=False))[0:10]
    elif engine == "solr":
        not_indexed_articles = Article.objects.filter(Q(article_text=None) | Q(article_text__indexed_by_solr=False))[0:10]
    else:
        return HttpResponse("The search engine name is not correct")

    print(not_indexed_articles)

    articles_json_data = []

    for article in not_indexed_articles:
        try:
            tmp = article.article_text
        except:
            article_text = ArticleText(article=article, text=__get_article_text(article))
            article_text.save()
        article_dict = {
            'id': article.id,
            'title': article.title,
            'text': article.article_text.text,
            'publish_time': article.publish_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        if engine == "es":
            article.article_text.indexed_by_es = True
        elif engine == "solr":
            article.article_text.indexed_by_solr = True
        article.article_text.save()
        
        articles_json_data.append(article_dict)

    return JsonResponse(get_json_dict(data=articles_json_data))
