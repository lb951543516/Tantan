#!/bin/bash

# 平滑重启 (不间断重启)

# 0. 初始状态
#     37898 主进程
#     40001 工作进程 <- 0
#     40002 工作进程 <- 0
#     40003 工作进程 <- 0
#     40004 工作进程 <- 0
# 1. 执行 `kill -HUP 37898`
# 2. 首先创建 一批新的工作进程
#     50001 工作进程 <- 12
#     50002 工作进程 <- 35
#     50003 工作进程 <- 73
#     50004 工作进程 <- 69
# 3. 新的用户请求，全部由新的工作进程处理，旧的工作进程不再接收用户请求
# 4. 当旧的工作进程全部处理结束后，会自动退出
# 5. 从始至终，主进程不会发生变化，主进程不接受用户请求，只对工作进程进行管理


echo '正在重启服务器'

PROJECT_DIR='/Tantan2003/Tantan'
PID_FILE="$PROJECT_DIR/logs/gunicorn.pid"

if [ -f $PID_FILE ]; then
    PID=`cat $PID_FILE`
    kill -HUP $PID
    echo '程序已重启完毕'
else
    echo '程序尚未启动，直接调用启动脚本'
    $PROJECT_DIR/scripts/start.sh
fi