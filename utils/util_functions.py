import json
import hashlib

from main.models import Section, Article

def get_article_dict(article):    
    """
    article is an instance of Article
    ret: 
    ARTICLE: {
      'id': <int>,
      'title': <str>,
      'section': <str>,
      'publish_time': <Y-m-d>,
      'images': [<str, image_url>, ...],
      'content': [
        {
          'type': <text/image>,
          'data': <str, text or image_url>
        }
      ]
    }
    """
    ret = {
        'id': article.id,
        'title': article.title,
        'section': article.section.name,
        'publish_time': article.publish_time.strftime("%Y-%m-%d %H:%M:%S"),
        'images': [article.image1_url, article.image2_url, article.image3_url],
        'content': json.loads(article.content),
    }

    while True:
        try:
            article_dict.remove(None)
        except:
            break;

    return ret

def get_user_dict(account):
    user_dict = {        
        'id': account.id,
        'nickname': account.nickname,
        'gender': account.gender,
        'icon': account.icon.url,
    }

def get_section_dict(section):
    section_dict = {
        'name': section.name,
        'description': section.description,
        'icon': section.icon.url,
        'creator': get_user_dict(section.creator),
    }

    return section_dict

def get_comment_dict(comment):
    comment_dict = {
        'user': get_user_dict(comment.creator),
        'time': comment.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        'content': comment.content,
    }

    return comment_dict

def get_md5(bytes):
    hash = hashlib.md5()
    hash.update(bytes)
    return hash.hexdigest()
