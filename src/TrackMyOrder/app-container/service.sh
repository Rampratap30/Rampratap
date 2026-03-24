#!/bin/bash
NAME="track-my-order-app"
HOST="0.0.0.0"
PORT="5000"
APP_DIR=/track-my-order/app-container
USER=tmoappuser

# how many worker processes should Gunicorn spawn (*)
NUM_WORKERS=2

# WSGI module name (*)
WSGI_MODULE=wsgi

cd $APP_DIR

SOCKFILE=/track-my-order/app-container/run/gunicorn.sock
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Flask Unicorn
exec gunicorn ${WSGI_MODULE} \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user $USER \
  --access-logfile=/track-my-order/log/gunicornlogs/access.log \
  --error-logfile=/track-my-order/log/gunicornlogs/error.log \
  --bind=$HOST:$PORT #\
#  --preload