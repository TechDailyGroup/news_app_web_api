from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from mind_graph.models import ArticleTags

from utils.api_utils import get_json_dict

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
    if request.user.username != "nlp":
        return HttpResponse("Permission Denied")

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
