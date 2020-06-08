#!/usr/bin/env bash

# requirements path
PARAM_REQUIREMENTS_PATH="./requirements.txt"

function install_requirements() {
  while read requirement; do pip install ${requirement}; done <${PARAM_REQUIREMENTS_PATH}
}

# config
function config() {
  case ${1} in
  "dev")
    bash ./config.sh "dev" || echo "config failed!"
    ;;
  "prod")
    bash ./config.sh "prod" || echo "config failed!"
    ;;
  *)
    echo "Expect prod/dev!"
    ;;

  esac
}
# run server
function start_service() {
  echo "try to start service for ${1}"
  python3 manage.py runserver || python manage.py runserver
}

case $1 in
install_requirements)
  install_requirements
  ;;
config)
  config "${2}"
  ;;
start_service)
  start_service "${2}"
  ;;
*)
  echo "usage: ./main.sh [install_requirements/config/start_service] [dev/prod]"
  ;;
esac
