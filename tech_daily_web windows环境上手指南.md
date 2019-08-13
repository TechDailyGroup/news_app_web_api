### tech_daily_web windows环境上手指南

**Note:** 把所有的资源（news_app_web_api, tech_daily_frontend, tech_daily_weeb_crawler）从TechDailyGroup fork 一份到自己的github, 然后pull 到本地进行修改。

[TOC]

#### 1. news_app_web_api

​		这部分是整个项目的后端，是一个以Django为基础的项目，从GitHub pull下来之后，经历以下操作：

##### 1.1 配置虚拟环境

​		我用的是Pycharm，在Pycharm 中打开项目并设置project interpreter，设置完成后，在terminal 使用`pip install -r requirements.txt`对requirements.txt中所要求的安装包进行逐一安装。如果出现某个版本的包无法安装，则手动安装即可。此外，还需要安装Django, pymysql ,corsheader等包。

​		安装完成后，需要更改Django项目关于数据库部分的配置：找到/news_app/settings.py文件，修改其中的内容。

>   1.  修改 ALLOWED_HOSTS
>   2.  修改DATABASES参数
>   3.  可能还有一些因为linux/windows环境差异引起的问题，在此不一一列举，可自行百度解决。

​		配置完成以后，命令行运行`python manage.py`，弹出以下内容：

```shell
Type 'manage.py help <subcommand>' for help on a specific subcommand.

Available subcommands:

[auth]
    changepassword
    createsuperuser

[contenttypes]
    remove_stale_contenttypes
    
[django]
    check
    compilemessages
    createcachetable
    dbshell
    diffsettings
    dumpdata
    flush
    inspectdb
    loaddata
    makemessages
    makemigrations
    migrate
    sendtestemail
    shell
    showmigrations
    sqlflush
    sqlmigrate
    sqlsequencereset
    squashmigrations
    startapp
    startproject
    test
    testserver

[sessions]
    clearsessions

[staticfiles]
    collectstatic
    findstatic
    runserver
```

​		用python命令运行managepy时，需要带上述参数，此时用`python manage.py runserver`即可启动服务；也可以通过Pycharm带参数运行。

​		启动服务后，控制台出现的 http://127.0.0.1:8000/点击打开后看出现page not found的错误，这是因为后端没有包含前端的代码。界面使用和修改将会在前端部分介绍。

##### 1.2 Postman请求测试

​		这是后端比较重要的测试环节。Postman是一个可以用api对服务器进行请求测试的工具（详情百度）。安装好Postman之后，打开后端项目的api.md文件。	

​		以log in 的请求测试为为例，log in的请求类型是POST，url是本地url+/account/login，所以在Postman对应的request栏中填写 http://127.0.0.1:8000/account/login/并设置为POST类型，在Body一栏中选定raw类型并设置为json格式，然后填入：

```json
{
	"username": <str>,
	"password": <str>,
}
```

**Note: json文本的key和value都是双引号！单引号会报错！**

​		填完以后，send request就会自动帮你测试请求，可以通过查看response验证该请求是否正确。

##### 1.3 数据上传

​		该部分是等爬虫收集完数据之后运行该部分的程序将数据上传的服务端。可以先弄明白web_crawler再回头看这一部分。

​		数据上传这部分，需要用到一个uploaded的表作为辅助，建表语句已经写好在爬虫文件夹下的create_table_for_webcrawler.sql文件下。

​		数据上传用到的代码主要在/utils/tech_daily_data_migration.py和/utils/api_mimes.py两个文件中。基本流程是与数据库建立连接，然后从pages表中获取converted_html的内容，经过解析后从本地目录将之前爬虫已经保存的json格式的数据上传到服务器。

>   **Note:**此处遇见的问题有：
>
>   1. api_mimes.py中url部分重复了一个“/”导致路径解析错误。
>   2. tech_daily_data_migration.py中HTML_ROOT_PATH填写的是之前爬虫爬完的converted_html存在本地的绝对路径
>   3. tech_daily_data_migration.py中get_unuploaded_articles方法中得到的converted_html_path的值未经解析，与Windows环境下的路径不符，此处只好依照web_crawler中tech_daily_crawler\src\com\zelkova\datacrawler\webcrawler\htmlconverter\components\HtmlConverterService.java这个文件中的getMD5ChildPath方法对html_path的分割方法写了一个get_separated_path方法，将converted_html_path再处理一遍得到正确路径。

#### 2. tech_daily_frontend

##### 2.1 配置环境

​		前端是一个以vue.js为主的项目，目前不需要安装什么依赖，打开pull下来的项目，然后找到/src/service/URLS.js文件，修改第一栏的两行，把var origin 和var host改成后端运行的url (Django在本地是 http://127.0.0.1:8000/)。

##### 2.2 连接服务端

​		打开README.md找到 Build Setup部分，按照提示运行`npm run dev`即可，然后浏览器打开 http://localhost:8080能看见项目的前端啦（确实颜值一般hhh）

​		Build Setup部分以后还有大用，先不管。

##### 2.3 todo

需要重写界面。

#### 3. tech_daily_web_crawler

##### 3.1 下载依赖

​		爬虫依赖的包在https://fdugeek.com/static/tech_daily_web_crawler_libs.tar.gz可以下载，另外还需要一个windows的phantomjs。下载完成以后，解压到工作目录下。

​		打开sample.properties文件，更改对应的信息：

>   1.  修改phantomjs_driver_path
>   2.  修改html_saving_path（把路径改为新建立的目录路径）
>   3.  修改database部分的对应信息

##### 3.2 更新数据库

​		为了调试方便，我建立了一个本地的MySQL数据库，建表的脚本是create_table_for_crawler.sql，里面是建立pages和uploaded两张表的sql语句。然后把信息更新在sample.properties文件对应处。

##### 3.3 运行爬虫

​		爬虫整个流程大致分为四步工作：urlcrawler, htmlcrawler,  htmlparser, htmlconverter，对应的参数全都在sample.properties中配置好。main.sh是一个执行脚本，但是受限于Windows工作环境无法使用。因此我们需要分别运行这四个步骤，将urlcrawler, htmlcrawler,  htmlparser, htmlconverter分别配上 sample.properties组成双参数运行/src/com.zelkova.datacrawler.webcrawler/Main.java程序，然后进行工作。爬虫四个步骤完成后，可以在数据库中看到爬下来的数据，并且可以看到之前创建的存放converted_html的目录下已经装了不少文件。这些文件在之后的数据上传时需要用到。

#### 4. Pycharm/IDEA 使用指南

##### 4.1 连接数据库

##### 4.2 带参数运行

##### 4.3 远程debug



#### 5. deploy on server

sudo apt-get install libmysqlclient-dev