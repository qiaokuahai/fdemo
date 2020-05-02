# /bin/bash

project_dir="/root/workspace/fdemo"
cd ${project_dir}
. venv/bin/activate
echo "enter env success"

start(){
    ps -ef | grep gunicorn | awk '{print $2}' | xargs kill -9
    gunicorn -c gunicorn_gevent.py main:app
    echo "start api via gunicorn_gevent"
}

stop(){
    ps -ef | grep gunicorn | awk '{print $2}' | xargs kill -9
    echo "stop gunicorn_gevent api"
}

if [ $1 = "start" ];then
    start
elif [ $1 = "stop" ];then
    stop
else
    echo "input param does not exists!"
fi
