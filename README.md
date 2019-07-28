# Introduction

This is the backend of a news app

# Release Notes

## Release 1.1.8 (2018-09-13)

* Add support for CI/CD, including:
  * Dockerfile
  * Kubernetes deployment yaml file
  * Parameterized settings
* minor fix

## Release 1.1.7 (2018-09-03)

* Change the way search engine uses to access data

## Release 1.1.6 (2018-09-02)

* Fix a performance issue for external_data_access

## Release 1.1.5 (2018-09-2)

* Add user_actions model
* Add index for models in external_data_access

## Release 1.1.4 (2018-08-28)

* Add search function

## Release 1.1.3 (2018-07-16)

* Fix timezone issue
* bug fixes

## Release 1.1.2 (2018-07-06)

* Update requirements.txt
* Add API to get section detail
* Add section detail to ARTICLE
* bug fixes

## Release 1.1.1 (2018-06-20)

* Add comment APIs
* Add 'like the article' APIs

## Release 1.1 (2018-06-08)

* Add WeChat login API
* Add icon related APIs
* Add functions to change article, section and user details
* Add a function of getting hot sections

# APIs

Please refer to the api.md

# Development

## Required Softwares

1. Git
2. Python3
3. (Optional) Postman (This is used to make manual requests to your WebAPI)

## Prepare

1. Clone the repo into your local folder, enter the folder
2. Run `pip install -r requirements.txt` to install package dependencies
3. Run `python3 manage.py migrate` to setup your database
4. Run `python3 manage.py runserver 0.0.0.0:8000` to start the server