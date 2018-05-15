import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from account.models import *
from main.models import *
from utils.api_utils import get_json_dict
from utils.util_functions import get_article_dict, get_section_dict


@require_GET
def get_subscribed_sections(request):
    """
    USER: {
      id: <str>,
      nickname: <str>,
      gender: <str, 'M'/'F'>
    }
    SECTION: {
      name: <str>,
      creator: USER,
      description: <str>
    }
    {
      sections: [SECTION],
    }
    """

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
    
    for section in account.created_sections:
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

    section = request.GET['section']
    page = int(request.GET.get('page', 0))

    json_dict = get_json_dict(data={})
    json_dict['data']['articles'] = []

    for article in Article.objects.filter(section__name=section)[ONE_PAGE_SIZE*page: ONE_PAGE_SIZE*(page+1)]:
        json_dict['data']['articles'].append(get_article_dict(article))
        

    return JsonResponse(json_dict)

@require_GET
def get_article_content(request):
    article_id = request.GET['id']

    article = Article.objects.get(id=article_id)
    json_dict = get_json_dict(data={})
    json_dict['data']['article'] = get_article_dict(article)
    
    return JsonResponse(json_dict)

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
def publish_article(request):
    received_data = json.loads(request.body.decode('utf-8'))
    title = received_data['title']
    section = received_data['section']
    content = received_data['content']

    section = Section.objects.get(name=section)
    account = request.user.account

    if (section.creator != account):
        return JsonResponse(get_json_dict(err_code=-1, message="No Permission", data={}))
    
    new_article = Article(section=section, title=title, content=json.dumps(content), )
    images = [x["data"] for x in content if x["type"] == "image"]
    while len(images) < 3:
        images.append(None)
    new_article.image1_url = images[0]
    new_article.image2_url = images[1]
    new_article.image3_url = images[2]
    
    new_article.save()

    return JsonResponse(get_json_dict(data={}))

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
