import time
import json
from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from account.models import *
from main.models import *
from utils.api_utils import get_json_dict, get_permission_denied_json_dict
from utils.util_functions import get_article_dict, get_section_dict, get_md5, get_comment_dict

def __update_article_images(article):
    content = json.loads(article.content)
    images = [x["data"] for x in content if x["type"] == "image"]
    while len(images) < 3:
        images.append(None)
    article.image1_url = images[0]
    article.image2_url = images[1]
    article.image3_url = images[2]
    
    article.save()


@require_GET
def get_subscribed_sections(request):
    json_dict = get_json_dict(data={})
    
    user = request.user
    sections = []
    default_sections = ["TechDaily"]
    if (user.is_authenticated):
        account = user.account
        for section in account.subscribed_sections.all():
            sections.append(section)
    if len(sections) == 0:
        for section in default_sections:
            sections.append(Section.objects.get(name=section))

    json_dict['data']['sections'] = []
    for section in sections:
        json_dict['data']['sections'].append(get_section_dict(section))

    return JsonResponse(json_dict)

@login_required
@require_GET
def get_created_sections(request):
    json_dict = get_json_dict(data={})
    account = request.user.account

    json_dict['data']['sections'] = []
    
    for section in account.created_sections.all():
        json_dict['data']['sections'].append(get_section_dict(section))

    return JsonResponse(json_dict)

@require_GET
def get_hot_sections(request):
    json_dict = get_json_dict(data={})
    hot_sections = Section.objects.filter()[0:10] # TODO - fake function

    json_dict['data']['sections'] = []

    for section in hot_sections:
        json_dict['data']['sections'].append(get_section_dict(section))

    return JsonResponse(json_dict)
    

@require_GET
def get_article_list(request):
    """
    {
      'articles': [ARTICLE, ...]
    }
    """

    ONE_PAGE_SIZE = 10

    section = request.GET.get('section', "")
    page = int(request.GET.get('page', 0))

    json_dict = get_json_dict(data={})
    json_dict['data']['articles'] = []

    if section == "":
        articles = Article.objects.all().order_by('-publish_time')[ONE_PAGE_SIZE*page: ONE_PAGE_SIZE*(page+1)]
    else:
        articles = Article.objects.filter(section__name=section).order_by('-publish_time')[ONE_PAGE_SIZE*page: ONE_PAGE_SIZE*(page+1)]

    for article in articles:
        json_dict['data']['articles'].append(get_article_dict(article))
        

    return JsonResponse(json_dict)

@require_POST
@login_required
def like_the_article(request):
    """
    request: {
      "article_id": <int>
    }
    """
    received_data = json.loads(request.body.decode('utf-8'))
    article_id = received_data['id']

    account = request.user.account
    article = Article.objects.get(id=article_id)

    try:
        article.likers.get(user__username=account.user.username)
        article.likers.remove(account)
        message = "Undo like success"
    except:
        article.likers.add(account)
        message = "Like success"
    article.save()

    return JsonResponse(get_json_dict(data={}, message=message))

@require_GET
def user_like_article_or_not(request):
    article_id = request.GET['id']
    user = request.user

    like = False

    if user.is_authenticated:
        account = user.account
        try:
            article = account.liked_articles.get(id=article_id)
            like = True
        except:
            pass

    return JsonResponse(get_json_dict(data={'like': like}))

    
@require_GET
def get_recommended_article_list(request):
    # TODO - implement this function, now its fake

    return get_article_list(request)

@require_GET
def get_article_content(request):
    article_id = request.GET['id']

    article = Article.objects.get(id=article_id)
    json_dict = get_json_dict(data={})
    json_dict['data']['article'] = get_article_dict(article)
    
    return JsonResponse(json_dict)

@require_POST
def change_article(request):
    received_data = json.loads(request.body.decode('utf-8'))
    article_id = received_data['id']
    article_title = received_data['title']
    article_content = received_data['content']

    article = Article.objects.get(id=article_id)
    if article.section.creator != request.user.account:
        return JsonResponse(get_permission_denied_response())

    article.title = title
    article.content = json.dumps(article_content)
    article.save()
    __update_article_images(article)

    return JsonResponse(get_json_dict(data={}))

@login_required
@require_POST
def create_new_section(request):
    received_data = json.loads(request.body.decode('utf-8'))
    name = received_data['name']
    description = received_data['description']
    account = request.user.account

    new_section = Section(creator=account, name=name, description=description)
    new_section.save()
    new_section.subscribers.add(account)

    return JsonResponse(get_json_dict(data={}))

@login_required
@require_POST
def change_section_detail(request):
    received_data = json.loads(request.body.decode('utf-8'))
    old_section_name = received_data['old_section_name']
    description = received_data['description']
    new_section_name = received_data['new_section_name']
    account = request.user.account
    try:
        section = account.created_sections.get(name=old_section_name)
    except:
        return JsonResponse(get_permission_denied_json_dict())

    section.name = new_section_name
    section.description = description
    section.save()

    return JsonResponse(get_json_dict(data={}))

@login_required
@require_POST
def change_section_icon(request):
    picture = request.FILES['picture']
    section_name = request.POST['section']

    account = request.user.account
    try:
        section = account.created_sections.get(name=section_name)
    except Exception as e:
        return JsonResponse(get_permission_denied_json_dict())
        
    picture.name = "{timestamp}_{picture_name}".format(
        timestamp = int(round(time.time() * 1000)),
        picture_name = get_md5(picture.read())
    )

    section.icon = picture
    section.save()

    return JsonResponse(get_json_dict(data={}))
    

@login_required
@require_POST
def publish_article(request):
    received_data = json.loads(request.body.decode('utf-8'))
    title = received_data['title']
    section = received_data['section']
    content = received_data['content']

    # TODO - remove code block
    try:
        publish_time_str = received_data['publish_time']
        publish_time = datetime.strptime(publish_time_str, "%Y-%m-%d %H:%M:%S")
    except:
        publish_time = None
    # END TODO

    section = Section.objects.get(name=section)
    account = request.user.account

    if (section.creator != account):
        return JsonResponse(get_permission_denied_json_dict())
    
    new_article = Article(section=section, title=title, content=json.dumps(content), )
    new_article.save()

    __update_article_images(new_article)    
    
    # TODO - remove code block
    if publish_time != None:
        new_article.publish_time = publish_time
        new_article.save()
    # END TODO
    
    return JsonResponse(get_json_dict(data={}))

@login_required
@require_POST
def make_comment(request):    
    received_data = json.loads(request.body.decode('utf-8'))
    article_id = received_data['article_id']
    content = received_data['content']
    account = request.user.account
    article = Article.objects.get(id=article_id)
    comment = Comment(article=article, creator=account, content=comment)
    comment.save()

    return JsonResponse(get_json_dict(data={}))

@require_GET
def get_comments(request):
    
    article_id = int(request.GET['article_id'])
    page = int(request.GET['page'])
    
    ONE_PAGE_SIZE = 20
    st_index = page * ONE_PAGE_SIZE
    en_index = (page+1) * ONE_PAGE_SIZE
    
    comments = Comment.objects.filter(article__id=article_id).order_by('-create_time')[st_index, en_index]

    json_dict = get_json_dict(data={"comments": []})

    for comment in comments:
        json_dict['data']['comments'].append(get_comment_dict(comment))

    return JsonResponse(json_dict)

@require_GET
def search_for_sections(request):
    keyword = request.GET['keyword']
    
    sections = Section.objects.filter(name__contains=keyword)
    
    json_dict = get_json_dict(data={})
    json_dict['data']['sections'] = []

    for section in sections:
        json_dict['data']['sections'].append(get_section_dict(section))

    return JsonResponse(json_dict)

@login_required
@require_POST
def subscribe_section(request):
    received_data = json.loads(request.body.decode('utf-8'))
    section = received_data['section']
    section = Section.objects.get(name=section)

    section.subscribers.add(request.user.account)

    return JsonResponse(get_json_dict(data={}))

@login_required
@require_POST
def unsubscribe_section(request):
    received_data = json.loads(request.body.decode('utf-8'))
    section = received_data['section']
    section = Section.objects.get(name=section)

    section.subscribers.remove(request.user.account)

    return JsonResponse(get_json_dict(data={}))
