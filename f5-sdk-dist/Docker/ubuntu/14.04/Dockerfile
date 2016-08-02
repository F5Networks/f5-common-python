# Dockerfile
FROM ubuntu:trusty

RUN apt-get update && apt-get install -y \
	python-stdeb \
	fakeroot \
	python-all

COPY ./build-debs.sh /

