from django.http import JsonResponse
from django.views.decorators.http import require_GET

from account.models import Account, Action
from account.decorators import login_required
from main.models import Article, Comment
from utils.api_utils import get_json_dict
from utils.util_functions import get_article_dict, get_user_dict

@login_required
@require_GET
def get_score(request):

    account = request.user.account
    json_dict = get_json_dict(data={})
    json_dict["data"]["score"] = account.score    
    json_dict["data"]["rank"] = Account.objects.filter(score__gt=account.score).count() + 1

    return JsonResponse(json_dict)

@login_required
@require_GET
def get_actions(request):

    page = int(request.GET.get('page', 0))
    comments_per_page = 10

    comment_st = comments_per_page * page
    comment_en = comment_st + comments_per_page

    account = request.user.account
    actions = account.actions.order_by('-time')[comment_st:comment_en]

    json_dict = get_json_dict(data={'actions': []})
    for action in actions:
        action_data = {
            "type": action.type,
            "time": action.time.strftime("%Y-%m-%d %H:%M:%S")
        }
        if action.type == "read_article":
            article_id = int(action.value.split(":")[1])
            article = Article.objects.get(id=article_id)
            action_data["value"] = {
                'article_id': article_id,
                'article_title': article.title,
            }
        elif action.type == "make_comment":
            comment_id = int(action.value.split(":")[1])
            comment = Comment.objects.get(comment_id)
            action_data["value"] = {
                'comment_id': comment.id,
                'comment_content': comment.content,
                'article_id': comment.article.id,
                'article_title': comment.article.title,
            }
        else:
            continue

        json_dict['data']['actions'].append(action_data)

    return JsonResponse(json_dict)

@require_GET
def get_rank(request):

    page = int(request.GET.get('page', 0))
    accounts_per_page = 10

    account_st = accounts_per_page * page
    account_en = account_st + accounts_per_page

    accounts = Account.objects.order_by('-score')[account_st:account_en]

    json_dict = get_json_dict(data={'accounts': []})

    for account in accounts:
        json_dict['data']['accounts'].append(get_user_dict(account))

    return JsonResponse(json_dict)
