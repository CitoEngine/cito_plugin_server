#!/bin/bash
set -e
export DJANGO_SETTINGS_MODULE='cito_plugin_server.settings.production' 

LOGFILE=/opt/cito_plugin_server/logs/cito-webapp.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=2
PORT=9000
BIND_IP=0.0.0.0:$PORT

# user/group to run as
#USER=www-data
#GROUP=www-data

if [ $USER != "www-data" ]; then
    echo "!!!WARNING!! You should probably run this script with www-data"
    GROUP=$USER
fi


# switch to project dir, activate virtual environment
cd /opt/cito_plugin_server
source /opt/virtualenvs/citopluginvenv/bin/activate

test -d $LOGDIR || mkdir -p $LOGDIR

#This was the original command to start the app
#python manage.py run_gunicorn \
#        --workers $NUM_WORKERS \
#        --user=$USER --group=$GROUP \
#        --log-level=debug --log-file=$LOGFILE 2>>$LOGFILE --bind $BIND_IP

# This is the command for starting the app in dev mode
#python manage.py runserver $BIND_IP

# This is the workaround command for starting the app if run_gunicorn fails
gunicorn --workers=$NUM_WORKERS \
         --user $USER \
         --group $GROUP \
         --log-level=debug --log-file=$LOGFILE 2>>$LOGFILE --bind $BIND_IP \
         cito_plugin_server.wsgi
