FROM centos:6

RUN yum update -y && yum install rpm-build make tar python-setuptools -y

COPY ./build-rpms.sh /
