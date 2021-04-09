#!/bin/sh

login=$1
remotefolder=$2
user=$3
key=$4

if [ -z "$key" ]
then
    ssh $login "sudo chown -R $user $remotefolder"
else
    ssh -i $key $login "sudo chown -R $user $remotefolder" 
fi