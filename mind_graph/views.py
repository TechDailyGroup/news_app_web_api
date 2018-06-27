import json
from datetime import datetime, timedelta

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required

from main.models import Article
from mind_graph.models import ArticleTags

from utils.api_utils import get_json_dict
from utils.util_functions import get_article_dict

@login_required
@require_POST
def set_article_tags(request):
    """
    request: {
      "id": <int>,
      "tags": {
        "level1": <str>,
        "level2": <str>,
        "level3": <str>
      }
    }
    response: No data
    """
    if request.user.username != "TechDailyGroup":
        return HttpResponse("Permission Denied")

    print(request.body)
    received_data = json.loads(request.body.decode('utf-8'))
    article_id = int(received_data["id"])
    tags = received_data["tags"]
    level1_tag = tags["level1"]
    level2_tag = tags["level2"]
    level3_tag = tags["level3"]

    article = Article.objects.get(id=article_id)

    if not hasattr(article, 'article_tags'):
        article_tags = ArticleTags(
            article=article,
            level1_tag=level1_tag,
            level2_tag=level2_tag,
            level3_tag=level3_tag)
    else:
        article_tags = article.article_tags
        article_tags.level1_tag = level1_tag
        article_tags.level2_tag = level2_tag
        article_tags.level3_tag = level3_tag
        
    article_tags.save()

    return JsonResponse(get_json_dict(data={}))

@require_GET
def get_mind_graph(request):
    """
    request:
      time: %Y-%m-%d %H:%M:%S
    response:
      mind_graph: [{
        label1: <str>,
        label2: <str>,
        label3: <str>,
        count: int
      }, ...]
    """

    return JsonResponse(get_json_dict(data={}))
    
    try:
        time = datetime.strftime(request.GET[time], "%Y-%m-%d %H:%M:%S")
    except:
        time = datetime.now()

    one_day_interval = timedelta(days=1000)
        
    articles = Article.objects.filter(publish_time__lt=time, publish_time__gt=time-one_day_interval)

    mind_graph = []
    mind_graph_dict = {}

    for article in articles:
        if hasattr(article, 'article_tags'):
            key = '{0}#{1}#{2}'.format(
                article.article_tags.level1_tag,
                article.article_tags.level2_tag,
                article.article_tags.level3_tag
            )
            try:
                mind_graph_dict[key] += 1
            except:
                mind_graph_dict[key] = 1

    for key in mind_graph_dict:
        value = mind_graph_dict[key]
        l1_tag, l2_tag, l3_tag = key.split("#")
        mind_graph.append({
            'label1': l1_tag,
            'label2': l2_tag,
            'label3': l3_tag,
            'count': value
        })

    return JsonResponse(get_json_dict(data={'mind_graph': mind_graph}))

@require_GET
def get_mind_graph_article_list(request):
    
    l1_tag = request.GET['label1']
    l2_tag = request.GET['label2']
    l3_tag = request.GET['label3']

    articles = Article.objects.filter(article_tags__level1_tag=l1_tag, article_tags__level2_tag=l2_tag, article_tags__level3_tag=l3_tag)

    json_dict_data = []
    
    for article in articles:
        json_dict_data.append(get_article_dict(article))

    return JsonResponse(
        get_json_dict(
            data={
                'articles': json_dict_data
            }
        )
    )
