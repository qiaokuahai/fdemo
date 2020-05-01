# /bin/bash

res=`pip3 list | grep virtualenv`
echo "${res}"

if [ -z "${res}" ];then
    echo "virtualenv not exist"
    pip3 install virtualenv
else
    echo "virtualenv exist"
fi

echo "---start mkdir env dir---"

cd ..
echo "curr dir path is `pwd`"
env_folder="./venv"
if [ -d ${env_folder} ];then
    echo "env dir already exist"
else
    echo "env not create"
    virtualenv -p /usr/local/python36/bin/python3 ${env_folder}
    echo "env create success"
fi

echo "curr dir path is `pwd`"
. venv/bin/activate
echo "---enter python3 env success---"

echo "install python package"
pip3 install -r requirements.txt
