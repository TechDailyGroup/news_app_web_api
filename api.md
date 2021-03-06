# News APP Web API
**Note:** All keys in json format should use " " other than ' '.
All responses use the format below:

```json
{
	"err_code": <int, 0 means success, otherwise fail>,
	"message": <str, human-readable message replied from the server>,
	"data": <data, this part is different from api to api>
}
```

The response sections below only show you the `data` part of the reply. But remember, the complete response format is like above.

If there is "login required" following the request url, and if you are not logined, then the following response will be returned (with HTTP status code `403`):

```json
{
	"err_code": -1,
	"message": "Login Required",
	"data": {}
}
```

## Account

This part includes functions related to user account, like register, login and logout.

### POST /account/register/

Register a new user

#### request

```json
{
	"username": <str>,
	"password": <str>,
	"gender": <"M"/"F">,
	"nickname": <str>
}
```

#### response

No data

### POST /account/login/

Login

#### request

```json
{
	"username": <str>,
	"password": <str>
}
```

#### response

No data

### GET /account/logout/ (login required)

Logout Need to login first

#### request

No data

#### response

No data

### GET /account/detail/ (login required)

Get user detail information. Need to login first

#### request

No data

#### response

```json
{
	"username": <str>,
	"gender": <"M"/"F">,
	"nickname": <str>,
	"icon": <str, url of the icon>
}
```

### POST /account/change_detail/ (login required)

#### request

```json
{
	"nickname": <str>,
	"gender": <str, "M"/"F">
}
```

#### response

No data

### POST /account/change_icon/ (login required)

#### request

picture: <file, an image file>

#### response

```json
{
	"icon": <str, new icon url>
}
```

### POST /account/change_password/ (login required)

#### request

```json
{
	"old_password": <str>,
	"new_password": <str>
}
```

#### response

No data

## Main

### Macro Variables

Here are some frequently used data structures in the json response.

#### USER

```json
{
	"id": <int>,
	"nickname": <str>,
	"gender": <str, "M"/"F">,
	"icon": <str, url of the picture>,
	"score": <int>
}
```

#### SECTION

```json
{
	"name": <str>,
	"creator": USER,
	"description": <str>,
	"icon": <str, url of the picture>
}
```

#### ARTICLE_CONTENT_ELEMENT

```json
{
	"type": <text/image>,
	"data": <str, text or image url>
}
```

#### ARTICLE

```json
{
	"id": <int>,
	"title": <str>,
	"section": SECTION,
	"publish_time": <str, yyyy-mm-dd>,
	"images": [<str, image url>, ...],
	"content": [ARTICLE_CONTENT_ELEMENT, ...],
	"liker_count": <int>
}
```

#### COMMENT

```json
{
	"user": USER,
	"time": <str, YYYY-mm-dd>,
	"content": <str>
}
```

### GET /api/section/subscribed/

#### request

No data

#### response

If user doesn"t login or user subscribes no section, then some default sections are returned

```json
{
	"sections": [SECTION, ...]
}
```

### GET /api/section/created/ (login required)

#### request

No data

#### response

```json
{
	"sections": [SECTION, ...]
}
```

### GET /api/section/hot/

#### request

No data

#### response

```json
{
	"sections:" [SECTION, ...]
}
```

### POST /api/section/new/ (login required)

#### request

```json
{
	"name": <str>,
	"description": <str>
}
```

#### response

No data

### GET /api/section/detail/

#### request

section: <str>

#### response

```json
{
	"section": SECTION
}
```

### GET /api/section/search/

#### request

```
keyword: <str>
```

#### response

```json
{
	"sections": [SECTION, ...]
}
```

### POST /api/section/subscribe/

#### request

```json
{
	"section": <str>
}
```

#### response

No data

### POST /api/section/unsubscribe/

#### request

```json
{
	"section": <str>
}
```

#### response

No data

### POST /api/section/change/ (login required)

#### request

```json
{
	"old_section_name": <str>,
	"new_section_name": <str>,
	"description": <str>
}
```

#### response

No data

### POST /api/section/change_icon/ (login required)

#### request

picture: <file, an image file>
section: <str>

#### response

```json
{
	"icon": <str, new icon url>
}
```

### GET /api/article/list/

#### request

```
section: <str>
page: <int>
```

#### response

```json
{
	"articles": [ARTICLES, ...]
}
```

### GET /api/article/search/

#### request

```
keyword: <str>
page: <int>
```

#### response

```json
{
	"articles": [ARTICLE, ...]
}
```

### GET /api/article/recommended/

#### request

```
page: <int>
```

#### response

```json
{
	"articles": [ARTICLE, ...]
}
```

### GET /api/article/similar_articles/

#### request

```
id: <int>
```

#### response

```json
{
	"articles": [ARTICLE, ...]
}
```

### GET /api/article/content/

#### request

```
id: <int>
```

#### response

```json
{
	"article": ARTICLE
}
```

### POST /api/article/like/

#### request

```
{
	"id": <int>
}
```

#### response

No data

### GET /api/article/like_or_not/

#### request

```
id: <int>
```

#### response

```json
{
	"like": <boolean, true/false>
}
```

#### GET /api/article/liker/

#### request

article_id: <int>

#### response

```json
{
	'likers': [USER, ...]
}
```

### POST /api/article/new/ (login required)

#### request

```json
{
	"title": <str>,
	"section": <str>,
	"content": [ARTICLE_CONTENT_ELEMENT, ...]
}
```

#### response

No data

### POST /api/article/comment/new (login required)

#### request

```
{
	"article_id": <int>,
	"content": <str>
}
```

#### response

No data

### GET /api/article/comment/

#### request

article_id: <int>
page: <int>

#### response

```json
{
	"comments": [COMMENT, ...]
}
```

### POST /api/article/change/ (login required)

#### request

```json
{
	"id": <int>,
	"title": <str>,
	"content": [ARTICLE_CONTENT_ELEMENT, ...]
}
```

#### response

No data

### GET /api/suggested_words/

#### request

```
word: <str>
```

#### response

```json
{
	"suggested_words" = [<str>, ...]
}
```

## Picture Bed

### POST /picture_bed/upload/ (login required)

#### request

picture: <file, an image file>

#### response

```json
{
	"picture_url": <str, url of the picture>
}
```

## External Data Access

### GET /external_data_access/latest_articles/ (login required, username must be "TechDailyGroup")

#### request

```
section: <str>
count: <int>
```

#### response

```json
{
	"articles": [{
		    "id": <int>,
		    "title": <str>,
		    "text": <str>,
		    "publish_time": <str, YYYY-mm-dd>
	}, ...]
}
```

### GET /external_data_access/article/list/

#### request

id: <int>

count: <int>

#### response

```json
{
	"articles": [{
		    "id": <int>,
		    "title": <str>,
		    "text": <str>,
		    "publish_time": <str, YYYY-mm-dd>
	}, ...]
}
```

## Mind Graph

### POST /mind_graph/set_article_tags/ (login required, username must be "TechDailyGroup")

#### request

```json
{
	"id": <int>,
	"tags": {
		"level1": <str>,
		"level2": <str>,
		"level3": <str>
	}
}
```

#### response

No data

### GET /mind_graph/

#### request

```
time: <str, format of "%Y-%m-%d %H:%M:%S">
```

#### response

```json
"mind_graph": [{
	      "level1": <str>,
	      "level2": <str>,
	      "level3": <str>,
	      "count": int
}, ...]
```

### GET /mind_graph/article_list/

#### request

```
label1: <str>
label2: <str>
label3: <str>
time: <str, format of "%Y-%m-%d %H:%M:%S">
```

#### response

```json
{
	"articles": [ARTICLE, ...]
}
```

## User Actions

### GET /user_actions/score/ (login required)

#### request

No data

#### response

```json
{
	"score": <int>,
	"rank": <int>
}
```

### GET /user_actions/actions/ (login required)

#### request

```
page: <int>
```

#### response

```json
{
	"actions": [ACTION, ...]
}

ACTION = {
	"type": <str, read_article/make_comment>,
	"time": <str, format of "%Y-%m-%d %H:%M:%S">,
	"value": {
		"comment_id": <int>,
		"comment_content": <str>,
		"article_id": <id>,
		"article_title": <str>
	}
}
```

### GET /user_actions/rank/

#### request

```
page: <int>
```

#### response

```json
{
	"users": [USER, ...]
}
```

## Wechat API

### POST /wechat_api/login/

#### request

```
{
        "code": <str>,
	"nickname": <str>
}
```

#### response

```
{
	"sessionid": <str>
}
```