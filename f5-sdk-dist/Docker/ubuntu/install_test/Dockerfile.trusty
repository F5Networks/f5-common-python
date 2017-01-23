# Dockerfile
FROM ubuntu:trusty

RUN apt-get update -y && apt-get install software-properties-common -y
# liberty does not have python-six 1.10.0+
RUN apt-add-repository cloud-archive:liberty
RUN apt-get update -y && apt-get dist-upgrade -y --force-yes
RUN apt-get install python-requests git curl -y --force-yes
RUN apt-get install python-six

COPY ./fetch_and_install_deps.py /

RUN chmod 700 /fetch_and_install_deps.py
ENTRYPOINT ["/fetch_and_install_deps.py", "/var/wdir"]
# The following is the default, last arg if you ran the docker container on its own...
CMD ["/var/wdir/f5-sdk-dist/deb_dist/python-f5-sdk_*_1404_all.deb"]
