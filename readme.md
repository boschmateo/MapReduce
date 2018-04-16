# Map reduce with PyActor

[![Build Status](https://travis-ci.org/boschmateo/MapReduce.svg?branch=master)](https://travis-ci.org/boschmateo/MapReduce) [![codecov](https://codecov.io/gh/boschmateo/MapReduce/branch/master/graph/badge.svg)](https://codecov.io/gh/boschmateo/MapReduce) [![codebeat badge](https://codebeat.co/badges/f6ec18b8-c5b5-4434-b0f9-f8d4271cb997)](https://codebeat.co/projects/github-com-boschmateo-mapreduce-master)

This project allows you to use a simplified prototype of the **MapReduce** model in python using [PyActor](https://github.com/pedrotgn/pyactor), *the minimalisistic python actor middleware*.

It supports two very simple programs:

 - **Counting words**: Counts the total number of words in a text file. For example, given the following text: "I love Distributed Systems", the output of CountingWords should be **4 words**.
 - **Word counting**: Counts the number of occurrences of each word in a text file. For instance, given the following text: "foo bar bar foo", the output of WordCount should be: **bar, 2; foo, 2**.

In both cases it will also show the time it took to process all the data.

## Installation
This projects uses the library PyActor which you can install using:

    pip install pyactor
Otherwise you just can clone this repoitory and install everything using:

    python setup.py install

## Tutorial
This project supports both sequential and distributed.


**Sequential mode**
An example for sequential can be found in examples:

    python examples/sequential.py <mode> <path to file>
As said before mode should be **CW** (counting words) or **WC** (word counting).

**Distributed mode**
First of all we will need to partition the file with the number of mappers that we want. Each file will be placed in the main directory of this project. It can be done by using:

    ./splitFile.sh <path to file> <number of partitions>

This will create N files with the name N.part.
Then we need to start the HTTP server to allow the hosts get their partitions:

    python -m SimpleHTTPServer
Now we have to create as many hosts as we want, for example using:

    python examples/hosts.py <port number>
This hosts can be created in any computer that has this repository cloned.
In this examples I will be using two hosts but it can be extrapolated to as many hosts as we want.
If you look at `examples/2mapper.py` you have to createa main host:

    host = create_host(IP_COMPUTER1+':1679')

An then lookup for the other hosts that you have created and then spawn the desired actor (in this case two mappers and one reducer):

    #Look for the host listening at the port 1277 and spawn a reducer
    reducerHost = host.lookup_url(IP_COMPUTER1 +':' + str(1277) + '/', Host)
    reducer = reducerHost.spawn(1277, Reduce)
    reducer.setNumberOfMappers(2)
    
    #Look for the host listening at the port 1278 and spawn a mapper
    remoteHost = host.lookup_url(IP_COMPUTER1 +':' + str(1278) + '/', Host)
    host1 = remoteHost.spawn(1278, Map)
    
    #Look for the host listening at the port 1279 and spawn a mapper
    remoteHost = host.lookup_url(IP_COMPUTER2 +':' + str(1279) + '/', Host)
    host2 = remoteHost.spawn(1279, Map)

All this ports are arbitrary.

Then all we need to do is call the map function from `host1` and `host2`

    # 8000 is the default port for the HTTP server
    host1.map(mode, IP_COMPUTER1+':8000/' + str(0) + ".part", reducer)
    host2.map(mode, IP_COMPUTER1+':8000/' + str(1) + ".part", reducer)

We will pas the reference of the reducer to the mappers. When they finish they will call the reducer actor with all the collected data and will process it.
When the reducer is finished processing the data it will output the CW or WC alongside the time it took to do so.

The examples directory contains more example files for doing so with 2,3,4 or 5 mappers.



#Documentation

You can read the full documentation (Catalan) in `documentacio.pdf` for more insight in the architecture, implementation and validation with speedups.