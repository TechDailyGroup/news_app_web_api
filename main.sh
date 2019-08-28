#!/usr/bin/env bash

# environment
PARAM_ENVI="dev"

# github params
GITHUB_REPO="https://github.com/CodeinSimon/news_app_web_api.git"

BRANCH_NAME="dev"

# requirements path
PARAM_REQUIREMENTS_PATH="./requirements/dev.txt"

# clone source code
function git_clone() {
  echo "Clone souce code from ${GITHUB_REPO} ${BRANCH_NAME}"
  git clone -b ${BRANCH_NAME} ${GITHUB_REPO} || echo "Error occurs when cloning!"
}

# install requirements
function install_requirements() {
  cd news_app_web_api || echo "no such directory!"
  echo "install requirements"
  pip3 install -r ${PARAM_REQUIREMENTS_PATH} || echo "pip requirements install failed"
}

# config
function config() {
  echo "Config settings"
  ./config.sh ${PARAM_ENVI} || echo "config failed!"
}
# run server
function start_service() {
    echo "start service"
    python3 manage.py runserver
}

git_clone
install_requirements
config
start_service


