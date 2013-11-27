#!/bin/bash
#coding=utf-8

#raspberry pi watchdog script
#author:kK

#interval
interval=30s;

#change to cuurent dir
cd `dirname $0`;

function check_internet_connection()
{
    baidu_header=`curl -I -s http://www.baidu.com`;
    if [ $? -ne 0 ];then
        return 1;
    fi
    headers=($baidu_header);
    if [ ${headers[1]} -eq 200 ];then
        return 0;
    else
        return 1;
    fi
}

echo "Raspi ddns started.";
internet_connection=0;
while :; do
    if check_internet_connection; then
        if [ $internet_connection -eq 0 ];then
            echo "Internet connection established.$`date`"
            internet_connection=1;
        fi
        if [[ $1 == "-systemd" ]]; then
            echo `python3 ddns.py -systemd`;
        else
            python3 ddns.py >> /dev/null
        fi
        if [ $? -ne 0 ];then
            echo "ddns tool error.";
        fi
    else
        if [ $internet_connection -ne 0 ];then
            echo "No internet connection. $`date`" >> /dev/stderr
            internet_connection=0;
        fi
    fi
    sleep $interval;
done;

