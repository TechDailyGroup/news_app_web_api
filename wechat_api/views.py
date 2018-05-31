import json
import requests
import random

from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse

from account.models import Account
from utils.api_utils import get_json_dict

appid = "wx3b7c3119a02b6eb6"
app_secret = "731c70d6da8e17b16069a6093b8dbd0f"
official_login_api_template = "https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={app_secret}&js_code={code}&grant_type=authorization_code"

def wechat_login(request):

    def __generate_random_password():
        ret = ""        
        for i in range(32):
            ret = ret + str(random.randint(0, 9))
        return ret
    
    received_data = json.loads(request.body.decode('utf-8'))
    code = received_data['code']

    official_login_api = official_login_api_template.format(
        appid=appid,
        app_secret=app_secret,
        code=code
    )

    response = requests.get(official_login_api)    

    response_dict = json.loads(response.text)

    print(response_dict)
    openid = response_dict['openid']
    session_key = response_dict['session_key']
    # unionid = response_dict['unionid']

    username = "wechat_{openid}".format(openid=openid)
    password = __generate_random_password()

    try:
        account = Account.objects.get(user__username=username)
        user = account.user
    except:
        user = User(username=username)
        user.set_password(password)
        user.save()
        account = Account(user=user, gender="F", nickname="WeCharUser")
        account.save()

    login(request, user)
    return JsonResponse(get_json_dict(data={"sessionid": request.session.session_key}))

def upload_picture(request):
    print(request.FILES['picture'].read())
    # print(request.body)
    # print(request.POST)
    return JsonResponse({})
