#!/bin/sh

login=$1
filen=$2
key=$3

ssh $key $login "rm $filen"
