import json

from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from account.models import Account
from account.forms import UserForm
from utils.api_utils import get_json_dict

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
    }

    json_dict['data'] = json_dict_data

    return JsonResponse(json_dict)
