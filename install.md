# Tech Daily Installation Document

[![platform](assets/Windows-brightgreen.svg)]()

>   This document records how to install this program on Windows and Linux.

In readme, we said that this program can be taken apart as three parts, so here you will see the installation in three parts and two different platforms.

**Tips: Before any installation, you should fork and download source code into your machine.**

## Table of Contents

-   [Installation on Windows](#Installation on Windows)
    -   [Part I. news_app_web_api](#Part I. news_app_web_api)
        -   [1.1 配置环境](#1.1 配置环境)
        -   [1.2 Postman请求测试](#1.2 Postman请求测试)
        -   [1.3 数据上传](#1.3 数据上传)
    -   [Part II. tech_daily_frontend](#Part II. tech_daily_frontend)
        -   [2.1 配置环境](#2.1 配置环境)
        -   [2.2 连接服务端](#2.2 连接服务端)
        -   [2.3 重写界面](#2.3 重写界面)
    -   [Part III. tech_daily_web_crawler](#Part III. tech_daily_web_crawler)
        -   [3.1 下载依赖](#3.1 下载依赖)
        -   [3.2 更新数据库](#3.2 更新数据库)
        -   [3.3 运行爬虫](#3.3 运行爬虫)
-   [Deploy on Linux Server](#Deploy on Linux Server)
    -   [Step 1. Config Database](#Step 1. Config Database)
        -   [1.1 下载安装包](#1.1 下载安装包)
        -   [1.2 操作步骤](#1.2 操作步骤)
    -   [Step 2. Deploy Frontend & Backend](#Step 2. Deploy Frontend & Backend)
        -   [2.1 操作步骤](#2.1 操作步骤)
        -   [2.2 注意事项](#2.2 注意事项)
    -   [Step 3. Deploy Crawler & Upload Data](#Step 3. Deploy Crawler & Upload Data)
        -   [3.1 操作步骤](#3.1 操作步骤)
    -   [Step 4. More Work in the Future](#Step 4. More Work in the Future)
        -   [4.1 TODO](#4.1 TODO)

## Installation on Windows

### Part I. news_app_web_api

​		这部分是整个项目的后端，是一个以Django为基础的项目，从GitHub pull下来之后，经历以下操作：

#### 1.1 配置环境

​		我用的是PyCharm，在PyCharm中打开项目并设置project interpreter，**请确保Python和pip都是3.x版本**。设置完成后，在terminal 使用`pip install -r requirements.txt`对requirements.txt中所要求的安装包进行逐一安装。如果出现某个版本的包无法安装，则手动安装即可。

​		安装完成后，需要更改Django项目关于数据库部分的配置：找到/news_app/settings.py文件，修改其中的内容。

>   1.  修改 ALLOWED_HOSTS
>   2.  修改DATABASES参数
>   3.  可能还有一些因为Linux/Windows环境差异引起的问题，在此不一一列举，可自行百度解决。

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

​		用python命令运行manage.py时，需要带上述参数，此时用`python manage.py runserver`即可启动服务；也可以通过PyCharm带参数运行。

​		启动服务后，控制台出现的 http://127.0.0.1:8000/点击打开后看出现page not found的错误，这是因为后端没有包含前端的代码。界面使用和修改将会在前端部分介绍。

#### 1.2 Postman请求测试

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

#### 1.3 数据上传

​		该部分是等爬虫收集完数据之后运行该部分的程序将数据上传的服务端。可以先弄明白web_crawler再回头看这一部分。

​		数据上传这部分，需要用到一个uploaded的表作为辅助，建表语句已经写好在爬虫文件夹下的create_table_for_crawler.sql文件下。

​		数据上传用到的代码主要在/utils/tech_daily_data_migration.py和/utils/api_mimes.py两个文件中。基本流程是与数据库建立连接，然后从pages表中获取converted_html的内容，经过解析后从本地目录将之前爬虫已经保存的json格式的数据上传到服务器。

>   **Note:** 此处遇见的问题有：
>
>   1. api_mimes.py中url部分重复了一个“/”导致路径解析错误。
>   2. tech_daily_data_migration.py中HTML_ROOT_PATH填写的是之前爬虫爬完的converted_html存在本地的绝对路径
>   3. tech_daily_data_migration.py中get_unuploaded_articles方法中得到的converted_html_path的值未经解析，与Windows环境下的路径不符，此处只好依照web_crawler中tech_daily_crawler\src\com\zelkova\datacrawler\webcrawler\htmlconverter\components\HtmlConverterService.java这个文件中的getMD5ChildPath方法对html_path的分割方法写了一个get_separated_path方法，将converted_html_path再处理一遍得到正确路径。
>   4. **第3条中的get_seperated_path仅在windows环境下需要使用，在linux环境要注释掉。**

### Part II. tech_daily_frontend

#### 2.1 配置环境

​		前端是一个以vue.js为主的项目，目前不需要安装什么依赖，打开pull下来的项目，然后找到/src/service/URLS.js文件，修改第一栏的两行，把var origin 和var host改成后端运行的url (Django在本地是 http://127.0.0.1:8000/)。

#### 2.2 连接服务端

​		打开README.md找到 Build Setup部分，按照提示运行`npm run dev`即可，然后浏览器打开 http://localhost:8080能看见项目的前端啦（确实颜值一般hhh）

​		Build Setup部分以后还有大用，先不管。

#### 2.3 重写界面

#TODO 需要重写界面。

### Part III. tech_daily_web_crawler

#### 3.1 下载依赖

​		爬虫依赖的包在https://fdugeek.com/static/tech_daily_web_crawler_libs.tar.gz可以下载，另外还需要一个windows的phantomjs。下载完成以后，解压到工作目录下。

​		打开sample.properties文件，更改对应的信息：

>   1.  修改phantomjs_driver_path
>   2.  修改html_saving_path（把路径改为新建立的目录路径）
>   3.  修改database部分的对应信息

#### 3.2 更新数据库

​		为了调试方便，我建立了一个本地的MySQL数据库，建表的脚本是create_table_for_crawler.sql，里面是建立pages和uploaded两张表的sql语句。然后把信息更新在sample.properties文件对应处。

#### 3.3 运行爬虫

​		爬虫整个流程大致分为四步工作：urlcrawler, htmlcrawler,  htmlparser, htmlconverter，对应的参数全都在sample.properties中配置好。main.sh是一个执行脚本，但是受限于Windows工作环境无法使用。因此我们需要分别运行这四个步骤，将urlcrawler, htmlcrawler,  htmlparser, htmlconverter分别配上 sample.properties组成双参数运行/src/com.zelkova.datacrawler.webcrawler/Main.java程序，然后进行工作。爬虫四个步骤完成后，可以在数据库中看到爬下来的数据，并且可以看到之前创建的存放converted_html的目录下已经装了不少文件。这些文件在之后的数据上传时需要用到。

## Deploy on Linux Server

### Step 1. Config Database

​		数据库单独一个服务器，放在`14`子服务器上。

#### 1.1 下载安装包

```bash
 sudo apt-get install mysql-server
 sudo apt-get install mysql-client
 sudo apt-get install libmysqlclient-dev
```

#### 1.2 操作步骤

1. 发送文件到主服务器 `scp deploy.sh **@**:/home/**`

2. 登陆主服务器，再发送到 数据库的服务器 `scp deploy.sh **@**:/home/**`

3. 登陆子服务器，安装git，mysql(已安装)等，配置public_key，添加到github，等。

4. 创建mysql用户:

    ```bash
    username: news_app
    password: ********
    ```

5. 登陆mysql `mysql -u news_app -p`，创建database: 

    ```bash
    database: news_app
    table name: news_app, web_crawler
    ```

6. 执行create_table_for_crawler.sql

    `source create_table_for_crawler.sql`

7. **设置database的character set为utf8。**

    > 1.修改mysql表的字符编码方式:
    > alter table t_name convert to character set utf8;
    > 2.修改数据库的字符集
    > alter database mydb character set utf8;
    > 3.创建数据库指定数据库的字符集
    > create database mydb character set utf8;

8. **设置数据库3306端口的可访问性，详见网络教程**

### Step 2. Deploy Frontend & Backend

​		前后端放在同一个服务器`14`上。

#### 2.1 操作步骤

1. 发送脚本和相关安装包到子服务器

2. 安装git, npm, node.js, python3, pip3 等，确保npm和nodejs是新版本。添加public_key到github。

3. 运行脚本clone 前后端仓库到服务器。

4. 运行脚本，配置后端的settings.py并且注意修改config.sh的相关信息（数据库等）

5. 数据库迁移
    `python3 manage.py migrate`

6. 创建Django超级用户

    >create superuser
    >
    >username: TechDailyGroup
    >
    >email: admin@fudan.edu.cn
    >
    >password: \*\*\*\*\*\*\*\*

7. 运行脚本部署后端

8. 运行脚本配置前端

    ```shell
    npm install
    npm run dev
    ```

#### 2.2 注意事项

1. 前端部分的npm使用方式见下:

```bash
# install dependencies
npm install
# serve with hot reload at localhost:8080
npm run dev
# build for production with minification
npm run build
# build for production and view the bundle analyzer report
npm run build --report
# add android platform:
cordova platform add android
# build the project(apk):
cordova build android
```

2. 前端的service/URL.js中的端口和host和后端的ALLOW_HOSTS需要相互对应。

### Step 3. Deploy Crawler & Upload Data

​		爬虫部署在服务器`17`。

#### 3.1 操作步骤

1. 从主服务器把脚本发给子服务器

2. 登陆子服务器，安装git，java，python3，pip3等环境，添加public_key到github。

3. 运行deploy.sh脚本，clone crawler和frontend的代码到本地。

4. 修改web_crawler的main.sh的脚本信息。

5. 在目录外root模式下运行deploy.sh，部署爬虫。

    > **Note: 爬虫的main.sh中的init_files函数会把爬虫的依赖包下载好，但是因为不可知原因下载有困难，建议把依赖包tech_daily_web_crawler_libs.tar.gz和phantomjs下载好scp到服务器上，注释掉init_files中wget的部分，并且把phantomjs解压好，解压后的文件夹名填写到main.sh中对应信息中。**

6. 可以用`bash main.sh status`查看已经部署好的爬虫状态。

7. 运行后端utils/tech_daily_data_migration.py文件前，需要修改文件中对应的数据库信息和API_HOST，爬虫存储的图片和json文件的路径信息等。

    > **Note: 在运行的时候可能会提醒服务器缺少mysql包，这时候用pip3安装即可。**
    >
    > **Warning: 之前在windows环境下写的get_unseparated_path函数在这里不用了，需要注释掉相关的引用部分。**

### Step 4. More Work in the Future

#### 4.1 TODO

1. 编写脚本，定时启动各项服务，自动拨号等等。
2. 重写前端。
3. 尽量把这些工作脚本化，服务后台化。