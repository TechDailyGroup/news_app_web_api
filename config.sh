#!/usr/bin/env bash
ORIGIN_SETTINGS_FILE=origin_settings.py
FINAL_SETTINGS_FILE=settings.py

# database
PARAM_MYSQL_DB_NAME=news_app
PARAM_MYSQL_USER=news_app
PARAM_MYSQL_PASSWORD=curidemo
PARAM_MYSQL_HOST=47.98.61.17
PARAM_MYSQL_PORT=13306

# SMTP
# PARAM_SMTP_HOST=param_smtp_host
# PARAM_SMTP_PORT=param_smtp_port
# PARAM_SMTP_FROM_ADDR=param_smtp_from_addr
# PARAM_SMTP_PASSWORD=password

# ALLOWED_HOST
PARAM_ALLOWED_HOST_DEBUG=("127.0.0.1" "118.24.52.60" "www.tech-daily.cn")
PARAM_ALLOWED_HOST_NOT_DEBUG=("127.0.0.1" "118.24.52.60" "www.tech-daily.cn")

HOST_STR1=" "
HOST_STR2=" "

# HOST
#PARAM_DEPLOY_HOST=param_deploy_host

# SECRET_KEY
PARAM_SECRET_KEY="p2^zm1jmbudhxi41lc6(t4d*%&a@rvp-7#igo-#^05+)27t=^@"

function config_dev() {
#  # SMTP
#  sed -i -e "s|param_smtp_password|${PARAM_SMTP_PASSWORD}|g" ${FINAL_SETTINGS_FILE}

  # ALLOWED HOST
  # shellcheck disable=SC2068
  for host in ${PARAM_ALLOWED_HOST_DEBUG[@]};
  do
    HOST_STR1=${HOST_STR1}"\"${host}\", "
  done
  sed -i -e "s|'param_debug_allowed_host'|${HOST_STR1}|g" ${FINAL_SETTINGS_FILE}

  # MYSQL
  sed -i -e "s|param_db_name|${PARAM_MYSQL_DB_NAME}|g" ${FINAL_SETTINGS_FILE}
  sed -i -e "s|param_db_user|${PARAM_MYSQL_USER}|g" ${FINAL_SETTINGS_FILE}
  sed -i -e "s|param_db_password|${PARAM_MYSQL_PASSWORD}|g" ${FINAL_SETTINGS_FILE}
  sed -i -e "s|param_db_host|${PARAM_MYSQL_HOST}|g" ${FINAL_SETTINGS_FILE}
  sed -i -e "s|param_db_port|${PARAM_MYSQL_PORT}|g" ${FINAL_SETTINGS_FILE}

  # DEPLOY_HOST
#  sed -i -e "s|param_deploy_host|$PARAM_DEPLOY_HOST|g" ${FINAL_SETTINGS_FILE}

  # SECRET_KEY
  sed -i -e "s|param_secret_key|${PARAM_SECRET_KEY}|g" ${FINAL_SETTINGS_FILE}
}

function config_prod() {
#  # SMTP
#  sed -i -e "s|param_smtp_password|${PARAM_SMTP_PASSWORD}|g" ${FINAL_SETTINGS_FILE}

  # DEBUG
  sed -i -e "s|DEBUG = True|DEBUG = False|g" ${FINAL_SETTINGS_FILE}

  # ALLOWED HOST
  # shellcheck disable=SC2068
  for host in ${PARAM_ALLOWED_HOST_NOT_DEBUG[@]};
  do
    HOST_STR2=${HOST_STR2}"\"${host}\", "
  done
  sed -i -e "s|'param_no_debug_allowed_host'|${HOST_STR2}|g" ${FINAL_SETTINGS_FILE}

  # MYSQL
  sed -i -e "s|param_db_name|${PARAM_MYSQL_DB_NAME}|g" ${FINAL_SETTINGS_FILE}
  sed -i -e "s|param_db_user|${PARAM_MYSQL_USER}|g" ${FINAL_SETTINGS_FILE}
  sed -i -e "s|param_db_password|${PARAM_MYSQL_PASSWORD}|g" ${FINAL_SETTINGS_FILE}
  sed -i -e "s|param_db_host|${PARAM_MYSQL_HOST}|g" ${FINAL_SETTINGS_FILE}
  sed -i -e "s|param_db_port|${PARAM_MYSQL_PORT}|g" ${FINAL_SETTINGS_FILE}

#  # DEPLOY_HOST
#  sed -i -e "s|param_deploy_host|$PARAM_DEPLOY_HOST|g" ${FINAL_SETTINGS_FILE}

  # SECRET_KEY
  sed -i -e "s|param_secret_key|${PARAM_SECRET_KEY}|g" ${FINAL_SETTINGS_FILE}

}

cd news_app || echo "cd news_app failed!"
cp ${ORIGIN_SETTINGS_FILE} ${FINAL_SETTINGS_FILE}

case $1 in
    dev)
  config_dev
  ;;
    prod)
  config_prod
  ;;
    *)
  echo "usage: ./config.sh <dev/prod>"
esac


