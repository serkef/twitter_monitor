#!/bin/sh

curPid=$(ps -ef | grep "python" | grep "twitter" | grep "monitor" | awk '{print $2}')

echo "Cloning last master"
rm -rf ${APP_HOME}
git clone --quiet https://github.com/serkef/twitter_monitor.git ${APP_HOME}
cp ${APP_HOME}/scripts/* $(dirname $0)

echo "Installing dependencies"
python3 -m venv ${APP_ENV}
. ${APP_ENV}/bin/activate
pip install -qqq wheel
pip install -qqq --upgrade -r ${APP_HOME}/requirements.txt

# Start the process again
echo "Starting monitor"
nohup python3 ${APP_HOME}/twitter_monitor/monitor.py &
echo "Killing previous version"
kill ${curPid}
