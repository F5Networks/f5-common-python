# Dockerfiles for testing the f5-sdk

This directory contains Dockerfiles that can be used to test the SDK.

## Building

To create the necessary docker images, you can use the following commands for...

Python 2

    docker build -f Dockerfile.python2 -t python2 .

And Python 3

    docker build -f Dockerfile.python2 -t python2 .

## Running

I use these on a Mac and found that they work as expected. Some explanation is
required

  * `docker run -it -v "${PWD}:/artifacts" --add-host="localhost:192.168.26.66" python2`
  * `docker run -it -v "${PWD}:/artifacts" --add-host="localhost:192.168.26.66" python3`

The `--add-host` argument lets me communicate with my host machine via that
IP address, but refer to it as "localhost".