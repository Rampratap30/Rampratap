#!/bin/bash
NAME="techMasterApi"
HOST="0.0.0.0"
PORT="5000"
APP_DIR=/tech-master/api-container

# the user to run as (*)
USER=apiuser

# how many worker processes should Gunicorn spawn (*)
NUM_WORKERS=2

# WSGI module name (*)
WSGI_MODULE=wsgi

cd $APP_DIR

SOCKFILE=/tech-master/api-container/run/gunicorn.sock
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Flask Unicorn
exec gunicorn ${WSGI_MODULE} \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user $USER \
  --access-logfile=/tech-master/log/gunicornlogs/access.log \
  --error-logfile=/tech-master/log/gunicornlogs/error.log \
  --bind=$HOST:$PORT \
  --preload