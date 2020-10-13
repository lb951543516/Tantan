#!/bin/bash

PROJECT_DIR='/Tantan2003/Tantan'

cd $PROJECT_DIR
workon tantan2003
gunicorn -c Tantan/gconfig.py Tantan/wsgi.py
deactivate

echo '程序启动'