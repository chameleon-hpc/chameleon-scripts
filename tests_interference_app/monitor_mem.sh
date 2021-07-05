#!/usr/local_rwth/bin/zsh

while ps -p $app_processID > /dev/null; 
do 
    ps -o pid,user,%mem,size -p $app_processID
    sleep 1; 
    #echo "running mem test"
done;