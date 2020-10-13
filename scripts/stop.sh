#!/bin/bash

PROJECT_DIR='/Tantan2003/Tantan'

PID_FILE="$PROJECT_DIR/logs/gunicorn.pid"

if [ -f $PID_FILE ]; then
    PID=`cat $PID_FILE`
    kill $PID
    echo '终止'
else
    echo '未启动'
fi