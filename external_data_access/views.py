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

@require_GET
def get_article_list(request):

    article_id_st = int(request.GET['id'])
    count = int(request.GET.get('count', 100))
    count = min(100, count)

    article_id_en = article_id_st + count

    articles = Article.objects.filter(id__gte=article_id_st, id__lt=article_id_en)

    json_dict = get_json_dict(data={"articles": []})

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
        json_dict['data']['articles'].append(article_dict)

    return JsonResponse(json_dict)
