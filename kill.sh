#!/bin/bash
# Roger Bosch Mateo, Jeroni Molina Mellado
# 28/03/2018
# ./kill.sh <numberOfHosts> <firstID>
# Script that kills N hosts

pid=$2
let number=$1+1
for i in $(seq 1 $number):
do
	kill $pid
	let pid=pid+1
done
