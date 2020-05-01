# /bin/bash

project_dir="/root/workspace/fdemo"
cd ${project_dir}
. venv/bin/activate
echo "enter env success"

start(){
    ps -ef | grep main.py | awk '{print $2}' | xargs kill -9
    nohup python3 main.py &
    echo "start api via python"
}

stop(){
    ps -ef | grep main.py | awk '{print $2}' | xargs kill -9
    echo "stop api"
}

if [ $1 = "start" ];then
    start
elif [ $1 = "stop" ];then
    stop
else
    echo "input param does not exists!"
fi
