#!/bin/bash

echo "usage - ./tunnel <loginname> <ip> <lport> <rport> <host>"

LOGIN=$1
IP=$2
LPORT=$3
RPORT=$4
HOST=$5
KEYPAIR=$6

if [ -z $LOGIN ] || [ -z $IP ] || [ -z $LPORT ] || [ -z $RPORT ] || [ -z $HOST ]; then
    echo "Args error !"
    exit 1
fi

if [ -z $KEYPAIR ]; then 
	KEYPAIR=""
else
	KEYPAIR=" -i ${KEYPAIR}"
fi

echo "keypair "$KEYPAIR

echo "Starting tunnel script..."

while true; do
	echo "Starting tunnel on "$HOST" via "$IP"...."
	ssh $KEYPAIR -o ConnectTimeout=4 -q $LOGIN@$IP -L $LPORT:$HOST:$RPORT -N
	echo "Tunnel error..retrying..."
	sleep 1
done
