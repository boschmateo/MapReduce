#!/bin/bash
# Roger Bosch Mateo, Jeroni Molina Mellado
# 28/03/2018
# ./kill.sh <numberOfHosts> <firstID>
# Script that kills N hosts

pid=$2
let number=$1+1

# Check number of arguments
if [ $# -ne 2 ]; then
    echo "ERROR: incorrect number of arguments"
	echo "Usage: ./kill.sh <numberOfHosts> <firstID>"
    exit 1
fi

if [ $pid -le 1000];then
	echo "No reventis el sistema paio..."
	echo "Usage: ./kill.sh <numberOfHosts> <firstID>"
	exit 1
fi

for i in $(seq 1 $number):
do
	kill $pid
	let pid=pid+1
done
