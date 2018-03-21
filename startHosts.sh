#!/bin/bash

if [ $# -eq 1 ]; then
	port=1277
	maxPort=$((1277 + $1))
	while [ $port -lt $maxPort ]; do

		(python "host.py" $port)&
		echo "Starting host $port"
		port=$(($port + 1))
		
	done

fi