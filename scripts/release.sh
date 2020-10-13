#!/bin/bash

USER='root'
HOST='119.45.201.6'
LOCAL_DIR='./' #要上传的文件夹
REMOTE_DIR='/Tantan2003/Tantan' #放到哪个文件夹里

# 切换指定版本
if [[ "$#" == "1" ]]; then
    git checkout $1
fi

#代码上传到服务器
rsync -crvP $LOCAL_DIR $USER@$HOST:$REMOTE_DIR --exclude={.git,venv,logs,__pycache__,vscode,.idea}

#重启服务器
read -p '你是否要重启服务器? (y/n)' result
if [[ $result == 'y' ]]; then
    ssh $USER@$HOST "$REMOTE_DIR/script/restart.sh"
fi