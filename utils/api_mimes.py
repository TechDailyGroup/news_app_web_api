import json
import requests
from datetime import datetime

class APIMimer:

    def __init__(self, api_host):
        self.API_HOST = api_host
        self.LOGIN_URL = "{0}/{1}".format(self.API_HOST, "/account/login/")
        self.UPLOAD_PICTURE_URL = "{0}/{1}".format(self.API_HOST, "/picture_bed/upload/")
        self.UPLOAD_ARTICLE_URL = "{0}/{1}".format(self.API_HOST, "/api/article/new/")
        self.session = requests.session()

    def __assert_response_valid(self, response):
        with open("response.html", "w") as f:
            f.write(response.text)
            f.close()
        response_dict = json.loads(response.text)
        assert(response.ok)
        print(response_dict['message'])
        assert(response_dict['err_code'] == 0)
        return response_dict

    def login(self, username, password):        
        json_dict = {
            "username": username,
            "password": password
        }
        response = self.session.post(self.LOGIN_URL, data=json.dumps(json_dict))
        self.__assert_response_valid(response)

    def upload_picture(self, file_abs_path):
        f = open(file_abs_path, "rb")
        files_dict = {
            'picture': f
        }

        response = self.session.post(self.UPLOAD_PICTURE_URL, files=files_dict)
        response_dict = self.__assert_response_valid(response)
        picture_url = response_dict['data']['picture_url']
        print("upload picture {0} success, url is {1}", file_abs_path, picture_url)
        return picture_url

    def upload_article(self, section, title, content, time):
        json_dict = {
            "section": section,
            "title": title,
            "content": content,
            "publish_time": str(time)
        }

        response = self.session.post(self.UPLOAD_ARTICLE_URL, data=json.dumps(json_dict))
        self.__assert_response_valid(response)
        print("upload article success, title is {0}".format(title))

if __name__ == "__main__":
    api_mimer = APIMimer("http://10.144.5.123")
    api_mimer.login("TechDailyGroup", "curidemo")
    print(api_mimer.upload_picture("/home/bz/tmp.jpg"))
