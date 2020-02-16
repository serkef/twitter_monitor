# twitter_monitor
Monitors twitter accounts


## How to develop
* Ensure you are on Python 3.7+ `python --version`
* Create a virtual environment`python -m venv venv/`
* [Install poetry](https://python-poetry.org/docs/#installation) 
* Install dependencies with poetry `poetry install`
* Run tests `pytest tests/`


## Archiving data to cloud
We have a [simple script](scripts/archive.sh) which compresses past fetched tweets and uploads them to 
the cloud of your choice using [rclone](https://rclone.org/).
* `RCLONE_PATH` env needs to be set and sets the path to rclone executable.
* `RCLONE_REMOTE` env needs to be set and sets the remote path. Make sure to first config rclone with your cloud settings

Example:
* `export RCLONE_PATH=/usr/bin/rclone`
* `export RCLONE_REMOTE="s3-twitter-monitor:twitter-monitor/data/"`


## Deployment
We have a simple deployment. For this you would need to install [webhook](https://github.com/adnanh/webhook) on the 
system that will run twitter monitor. Then we provide a [configuration](scripts/webhook.json) to listen to the webhook 
and a [deployment script](scripts/webhook-redeploy.sh) to redeploy the application. For those you will need to set:
* `GITHUB_WEBHOOK_SECRET` your github webhook secret (so that gh pushes are triggering redeployment)
* `DEPLOY_HOME` your project basic folder (where deployment can assume as cwd)
* `DEPLOY_SCRIPT` to point to our script
* `APP_HOME` is the path where twitter monitor will be installed
* `APP_ENV` is the path where virtual environment for twitter monitor will be installed
* `APP_LOGS` is the path where logs will be stored

Example:
* `export GITHUB_WEBHOOK_SECRET=xxx`
* `export DEPLOY_HOME=/home/ubuntu`
* `export DEPLOY_SCRIPT=/home/ubuntu/webhook-redeploy.sh`
* `export APP_HOME=/opt/twitter-monitor`
* `export APP_ENV=/opt/twitter-monitor/venv`
* `export APP_LOGS=/home/ubuntu/twimon-logs`


## 