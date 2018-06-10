#!/bin/bash
# Roger Bosch Mateo, Jeroni Molina Mellado
# 28/03/2018
# ./splitFile.sh <filename> <numberSubfiles>
# Script that split a file in N subfiles,  it will create the subfiles with the default name of xaa, xab, ...

function printUsage {
    echo "Usage: ./splitFile.sh <filename> <numberSubfiles>"
    echo "Script that split a file in N subfiles, it will create the subfiles with the default name of xaa, xab, ..."
}

# Check number of arguments
if [ $# -ne 2 ]; then
    echo "ERROR: incorrect number of arguments"
    printUsage
    exit 1
fi

filename=$1
numberSubfiles=$2

# Check if file exists
if [ ! -f $filename ];then
    echo "ERROR: file don't exist"
    printUsage
    exit 1
fi

# Check if number is less than 0
if [ $# -le 0 ]; then
    echo "ERROR: the number os subfiles must be greater than 0"
    printUsage
    exit 1
fi

# Check if exist previous files
if [ -f 0.part ];then
    # Remove previous files
    rm *.part
fi


# Split and create the subfiles
split -l  $(expr `wc $filename | cut -d ' ' -f3` / $2 + `expr $numberSubfiles - 1`) $filename

# Change name to numbers
count=0
for i in x??;
do
    ext=$count
    ext+=".part"
    mv $i $ext
    let count=count+1
done
