# News APP Web API

All responses use the format below:

```json
{
	'err_code': <int, 0 means success, otherwise fail>,
	'message': <str, human-readable message replied from the server>,
	'data': <data, this part is different from api to api>
}
```

The response sections below only show you the `data` part of the reply. But remember, the complete response format is like above.

## Account

This part includes functions related to user account, like register, login and logout.

### POST /account/register/

Register a new user

#### request

```json
{
	'username': <str>,
	'password': <str>,
	'gender': <'M'/'F'>,
	'nickname': <str>
}
```

#### response

No data

### POST /account/login/

Login

#### request

```json
{
	'username': <str>,
	'password': <str>
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
	'username': <str>,
	'gender': <'M'/'F'>,
	'nickname': <str>,
	'icon': <str, url of the icon>
}
```

### POST /account/change_detail/ (login required)

#### request

```json
{
	'nickname': <str>,
	'gender': <str, 'M'/'F'>
}
```

#### response

No data

### POST /account/change_icon/ (login required)

#### request

picture: <file, an image file>

#### response

No data

### POST /account/change_password/ (login required)

#### request

```json
{
	'old_password': <str>,
	'new_password': <str>
}
```

#### response

No data

## Main

### Macro Variables

Here are some frequently used data structures int the json response.

#### USER

```json
{
	'id': <int>,
	'nickname': <str>,
	'gender': <str, 'M'/'F'>,
	'icon': <str, url of the picture>
}
```

#### SECTION

```json
{
	'name': <str>,
	'creator': USER,
	'description': <str>,
	'icon': <str, url of the picture>
}
```

#### ARTICLE_CONTENT_ELEMENT

```json
{
	'type': <text/image>,
	'data': <str, text or image url>
}
```

#### ARTICLE

```json
{
	'id': <int>,
	'title': <str>,
	'section': <str>,
	'publish_time': <str, yyyy-mm-dd>,
	'images': [<str, image url>, ...],
	'content': [ARTICLE_CONTENT_ELEMENT, ...]
}
```

#### COMMENT

```json
{
	'user': USER,
	'time': <str, YYYY-mm-dd>,
	'content': <str>
}
```

### GET /api/section/subscribed/

#### request

No data

#### response

If user doesn't login or user subscribes no section, then some default sections are returned

```json
{
	'sections': [SECTION, ...]
}
```

### GET /api/section/created/ (login required)

#### request

No data

#### response

```json
{
	'sections': [SECTION, ...]
}
```

### GET /api/section/hot/

#### request

No data

#### response

```json
{
	'sections:' [SECTION, ...]
}
```

### POST /api/section/new/ (login required)

#### request

```json
{
	'name': <str>,
	'description': <str>
}
```

#### response

No data

### GET /api/section/search/

#### request

```
keyword: <str>
```

#### response

```json
{
	'sections': [SECTION, ...]
}
```

### POST /api/section/subscribe/

#### request

```json
{
	'section': <str>
}
```

#### response

No data

### POST /api/section/unsubscribe/

#### request

```json
{
	'section': <str>
}
```

#### response

No data

### POST /api/section/change/ (login required)

#### request

```json
{
	'old_section_name': <str>,
	'new_section_name': <str>,
	'description': <str>
}
```

#### response

No data

### POST /api/section/change_icon/ (login required)

#### request

picture: <file, an image file>
section: <str>

#### response

No data

### GET /api/article/list/

#### request

```
section: <str>
page: <int>
```

#### response

```json
{
	'articles': [ARTICLES, ...]
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
	'article': ARTICLE
}
```

### POST /api/article/new/ (login required)

#### request

```json
{
	'title': <str>,
	'section': <str>,
	'content': [ARTICLE_CONTENT_ELEMENT, ...]
}
```

#### response

No data

### POST /api/article/comment/new (login required)

#### request

```
{
	'article_id': <int>,
	'content': <str>
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
	'comments': [COMMENT, ...]
}
```

### POST /api/article/change/ (login required)

#### request

```json
{
	'id': <int>,
	'title': <str>,
	'content': [ARTICLE_CONTENT_ELEMENT, ...]
}
```

#### response

No data

## Picture Bed

### POST /picture_bed/upload/ (login required)

#### request

picture: <file, an image file>

#### response

```json
{
	'picture_url': <str, url of the picture>
}
```

## External Data Access

### GET /external_data_access/latest_articles/ (login required, username must be 'nlp')

#### request

```
section: <str>
count: <int>
```

#### response

```json
{
	'articles': [{
		    'id': <int>,
		    'title': <str>,
		    'text': <str>,
		    'publish_time': <str, YYYY-mm-dd>
	}, ...]
}
```

### GET /external_data_access/not_indexed_articles/ (login required, username must be 'nlp')

Notice: This is a API for search engine testing

#### request

engine: <str, "es"/"solr">

#### response

```json
{
	'articles': [{
		    'id': <int>,
		    'title': <str>,
		    'text': <str>,
		    'publish_time': <str, YYYY-mm-dd>
	}, ...]
}
```

## Mind Graph

### POST /mind_graph/set_article_tags/ (login required, username must be 'nlp')

#### request

```json
{
	'id': <int>,
	'tags': {
		'level1': <str>,
		'level2': <str>,
		'level3': <str>
	}
}
```

#### response

No data

### GET /mind_graph/

#### request

```
time: <str, format of '%Y-%m-%d %H:%M:%S'>
```

#### response

```json
'mind_graph': [{
	      'level1': <str>,
	      'level2': <str>,
	      'level3': <str>,
	      'count': int
}, ...]
```

### GET /mind_graph/article_list/

#### request

```
label1: <str>
label2: <str>
label3: <str>
```

#### response

```json
{
	'articles': [ARTICLE, ...]
}
```

## Wechat API

### POST /wechat_api/login/

#### request

```
{
        'code': <str>,
	'nickname': <str>
}
```

#### response

```
{
	'sessionid': <str>
}
```