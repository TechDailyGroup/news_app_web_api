import json
import time

from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

from account.models import Account
from account.forms import UserForm
from account.decorators import login_required
from utils.api_utils import get_json_dict
from utils.util_functions import get_md5

@require_POST
def user_register(request):
    request.POST = json.loads(request.body.decode('utf-8'))
    username = request.POST['username']
    password = request.POST['password']
    gender = request.POST['gender']
    nickname = request.POST['nickname']
    
    user_form_data = {
        'username': username,
        'password': password,
    }
    user_form = UserForm(data=user_form_data)

    json_dict = {
        'err_code': 0,
        'message': "Register success",
        'data': {}
    }
    
    if user_form.is_valid():
        user = user_form.save(commit=False)
        user.set_password(user.password)
        user.save()
        account = Account(
            user = user,
            gender = gender,
            nickname = nickname,
        )
        if gender == "M":
            account.icon = "default_pictures/male-default.png"
        else:
            account.icon = "default_pictures/female-default.png"
        account.save()
        return JsonResponse(json_dict)
    json_dict['err_code'] = -1
    json_dict['message'] = "User form is not valid"
    return JsonResponse(json_dict)
        
@require_POST
def user_login(request):
    request.POST = json.loads(request.body.decode('utf-8'))
    username = request.POST['username']
    password = request.POST['password']

    json_dict = {
        'err_code': 0,
        'message': "Login success",
        'data': {},
    }

    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return JsonResponse(json_dict)
    else:
        json_dict['err_code'] = -1
        json_dict['message'] = "Invalid username or password"
        return JsonResponse(json_dict)

@login_required
@require_GET
def user_logout(request):
    logout(request)
    json_dict = {
        'err_code': 0,
        'message': "Logout success",
        'data': {}
    }

    return JsonResponse(json_dict)

@login_required
@require_GET
def user_detail(request):
    account = request.user.account
    json_dict = get_json_dict(data={})

    json_dict_data = {
        'username': account.user.username,
        'gender': account.gender,
        'nickname': account.nickname,
        'icon': account.icon.url,
    }

    json_dict['data'] = json_dict_data

    return JsonResponse(json_dict)

@login_required
@require_POST
def change_detail(request):
    received_data = json.loads(request.body.decode('utf-8'))
    new_nickname = received_data['nickname']
    new_gender = received_data['gender']

    account = request.user.account
    account.nickname = new_nickname
    account.gender = new_gender
    account.save()

    return JsonResponse(get_json_dict(data={}))

@login_required
@require_POST
def change_password(request):
    received_data = json.loads(request.body.decode('utf-8'))
    old_password = received_data['old_password']
    new_password = received_data['new_password']

    user = authenticate(username=request.user.username, password=old_password)    
    if user:
        user.set_password(new_password)
        user.save()
        login(request, user)
        return JsonResponse(get_json_dict(data={}))
    else:
        return JsonResponse(get_json_dict(err_code=-1, message="Invalid Password", data={}))


@login_required
@require_POST
def change_icon(request):
    picture = request.FILES['picture']
    
    picture.name = "{timestamp}_{picture_name}".format(
        timestamp = int(round(time.time() * 1000)),
        picture_name = get_md5(picture.read())
    )

    account = request.user.account
    account.icon = picture
    account.save()

    return JsonResponse(get_json_dict(data={'icon': account.icon.url}))
    
