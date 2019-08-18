import os
import json
import time
import codecs
import re
# original = ""
# regex = re.compile(r'\\(?![/u"])')
# fixed = regex.sub(r"\\\\", original)

import pymysql

from utils.api_mimes import APIMimer

# here should be your data base info.
HOST = "192.168.160.49"
USERNAME = "root"
PASSWORD = "980929"
DATABASE = "web_crawler"

# your server host
# API_HOST = "http://118.24.52.60:8000"
API_HOST = "http://127.0.0.1:8000"
# absolute path
HTML_ROOT_PATH = os.path.abspath(
    "../..") + os.path.sep + "tech_daily_crawler" + os.path.sep + "converted_html_files" + os.path.sep
# print(HTML_ROOT_PATH)

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
                print("upload picture failed during preprocess!")
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


def get_separated_path(unseparated):
    """
    :param converted_html_path: a converted html path ending with "index.html"
    :return: a string adding os.path.sep
    :
    """
    # replace invisible characters
    print("before replace:", unseparated)
    test = ""
    for i in range(len(unseparated)):
        if not unseparated[i].isalpha() and not unseparated[i].isdigit():
            test += '0'
        else:
            test += unseparated[i]
    unseparated = test
    print("after replace:", test)
    try:
        # unseparated = unseparated[:-10]
        res = unseparated[0:1] + "/" \
              + unseparated[1:3] + "/" \
              + unseparated[3:6] + "/" \
              + unseparated[6:10] + "/" \
              + unseparated[10:-10] + "/" \
              + unseparated[-10:]
        return res
    except:
        # fix-me better error handling
        print("substring error!")
    return ""


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
        print("converted html path:", converted_html_path)
        print(len(converted_html_path))
        html_path = get_separated_path(str(converted_html_path))
        print("html path:", html_path)
        print(len(html_path))
        article_json_file_path = os.path.join(os.path.dirname(os.path.join(HTML_ROOT_PATH, html_path)),
                                              "article.json")
        # article_json_file_path = article_json_file_path.replace("\\", "/")
        article_dict = {
            'id': article_id,
            'title': title,
            'publish_time': post_time
        }
        try:
            print("article_json_file_path", article_json_file_path)
            # f = codecs.open(article_json_file_path, "r", "utf-8")
            f = codecs.open(article_json_file_path, "r", encoding='utf-8')
            """ fix bug: ValueError: Invalid \ escape
            """
            regex = re.compile(r'\\(?![/u"])')
            fixed = regex.sub(r"\\\\", f.read())
            content_json_dict = json.loads(fixed, strict=False)
            article_dict["content"] = content_json_dict
            ret.append(article_dict)
        except FileNotFoundError:
            print(FileNotFoundError)
            print("Failed, update index flag")
            update_index_flag(article_dict)
    # print(ret)
    return ret


if __name__ == "__main__":
    while True:
        articles = get_unuploaded_articles()
        # print(len(articles))
        if len(articles) == 0:
            print("Sleep for 10 mins")
            time.sleep(60 * 10)
        for article in articles:
            # print("come in here")
            try:
                print("now is going to preprocess")
                preprocess_article(article)
                # print("now is going to upload")
                upload_article(article)
            except:
                print("upload articles failed")
            update_index_flag(article)

