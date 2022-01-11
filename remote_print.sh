#!/usr/bin/bash
server_ip=192.168.178.69
remote_folder=/home/cod/to_print
file_name=$1
n_copies=$2

scp ./tmp/$file_name cod@$server_ip:$remote_folder > /dev/null
rm ./tmp/$file_name > /dev/null
ssh cod@$server_ip 'lp -n $n_copies $remote_folder/$file_name' > /dev/null