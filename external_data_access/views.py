from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse

from main.models import Article
from external_data_access.models import ArticleText
from utils.api_utils import get_json_dict

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
          "publish_time": <YYYY-mm-dd>
        },
        ...
      ]
    }
    """

    if request.user.username != "nlp":
        return HttpResponse("Permission Denied")

    print(dir(request.user))
    count = int(request.GET['count'])
    count = min(count, 1000)
    articles = Article.objects.filter().order_by('publish_time')[0:count]

    articles_json_data = []

    for article in articles:
        if article.article_text.text == None:
            article.article_text.text = __get_article_text(article)
            article.article_text.save()
        article_dict = {
            'id': article.id,
            'title': article.title,
            'text': article.article_text.text,
            'publish_time': article.publish_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        articles_json_data.append(article_dict)

    json_dict = get_json_dict(data={"articles": articles_json_data})

    return JsonResponse(json_dict)
