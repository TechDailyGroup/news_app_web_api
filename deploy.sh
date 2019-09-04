#!/bin/bash

# this script is used to clone code from github then try to install requirements,
# config settings and run dev/prod program.
# before running this script, you should gengerate a ssh key on your machine and
# add it to github.

# Github Repo info
PARAM_BACKEND_REPO="git@github.com:CodeinSimon/news_app_web_api.git"
PARAM_FRONTEND_REPO="git@github.com:CodeinSimon/tech_daily_frontend.git"
PARAM_CRAWLER_REPO="git@github.com:CodeinSimon/tech_daily_web_crawler.git"


function clone() {
  BRANCH=""
  REPO=""
  case ${1} in
    prod)
      BRANCH="master"
      ;;
    dev)
      BRANCH="dev"
      ;;
    *)
      echo "Expect <dev/prod>!"
      return 0
      ;;
    esac
  case ${2} in
    backend)
      REPO=PARAM_BACKEND_REPO
      ;;
    frontend)
      REPO=PARAM_FRONTEND_REPO
      ;;
    crawler)
      REPO=PARAM_CRAWLER_REPO
      ;;
    *)
      echo "Expect <backend/frontend/crawler>!"
      return 0
      ;;
  esac
  echo "begin to clone branch ${BRANCH} from repo:${REPO}"
  git clone -b ${BRANCH} ${REPO}
}

function deploy_backend() {
    cd news_app_web_api || echo "No such directory!"
    bash ./main.sh install_requirements || echo "install requirements failed!"
    bash ./main.sh config "${1}" || echo "config settings failed!"
    bash ./main.sh start_service || echo "backend service started failed.}"
}

case ${1} in
  clone)
    clone "${2}" "${3}"
    ;;
  deploy_backend)
    deploy_backend "${1}"
    ;;
  *)
  echo "usage: ./deploy.sh [prod/dev] [backend/frontend/crawler]"
  ;;
esac