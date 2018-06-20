import os
import json
import time
import codecs

import pymysql

from api_mimes import APIMimer

HOST = "10.144.5.123"
USERNAME = "web_crawler"
PASSWORD = "curidemo"
DATABASE = "web_crawler"

API_HOST = "http://10.144.5.123"

HTML_ROOT_PATH = "/var/www/html/"

apimimer = APIMimer(API_HOST)
apimimer.login("TechDailyGroup", "curidemo")
conn = pymysql.connect(HOST, USERNAME, PASSWORD, DATABASE, charset='utf8')
cursor = conn.cursor()

def preprocess_article(article):

    new_content = []

    for element in article["content"]:
        if element["type"] == "image":
            image_path = os.path.join(HTML_ROOT_PATH, element["data"])
            try:
                new_image_url = apimimer.upload_picture(image_path)
                element["data"] = new_image_url
                new_content.append(element)
            except:
                pass
        else:
            new_content.append(element)

    article["content"] = new_content

def upload_article(article):
    apimimer.upload_article("TechDaily", article['title'], article['content'], article['publish_time'])
    print("article {0} uploaded, title: {1}".format(article["id"], article["title"]))

def update_index_flag(article):    
    sql = """insert into uploaded (doc_id, flag) values(%s, %s)"""
    cursor.execute(sql, (article["id"], 1))
    conn.commit()
    print("article {0} index flag assigned, title: {1}".format(article["id"], article["title"]))
    
def get_unuploaded_articles():
    """
    return [
      {
        "id": <int>,
        "title": <str>,
        "publish_time": <datetime.datetime>
        "content": [{
          "type": <str, "text"/"image">,
          "data": <str, text or image url>
        }]
      },
    ]
    """

    ret = []

    sql = """select a.id, a.title, a.post_time, a.converted_html_path 
    from pages as a left join uploaded as b
    on a.id = b.doc_id
    where (b.flag is null) 
    and a.title is not null and not a.title = ''
    and a.converted_html_path is not null and not a.converted_html_path = ''
    and a.post_time is not null 
    order by post_time desc
    limit 10
    """
    cursor.execute(sql)

    for (article_id, title, post_time, converted_html_path) in cursor.fetchall():
       article_json_file_path = os.path.join(os.path.dirname(os.path.join(HTML_ROOT_PATH, converted_html_path)), "article.json")
       article_dict = {
           'id': article_id,
           'title': title,
           'publish_time': post_time
       }
       try:
           f = codecs.open(article_json_file_path, "r", "utf-8")
           content_json_dict = json.loads(f.read())
           article_dict["content"] = content_json_dict
           ret.append(article_dict)
       except:
           update_index_flag(article_dict)

    return ret


if __name__ == "__main__":
    while True:
        articles = get_unuploaded_articles()
        if len(articles) == 0:
            print("Sleep for 10 mins")
            time.sleep(60 * 10)
        for article in articles:
            try:
                preprocess_article(article)
                upload_article(article)
            except:
                pass
            update_index_flag(article)
