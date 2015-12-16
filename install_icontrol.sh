#!/bin/sh

# curl -L https://github.com/F5Networks/f5-icontrol-rest-python/archive/v0.1.0.tar.gz > /tmp/icontrol.tar.gz
# tar -zxf /tmp/icontrol.tar.gz -C /tmp
# mv /tmp/f5-icontrol-rest-python-0.1.0/icontrol/ .

echo -e "Installing iControlREST"

travis login --pro -u $TRAVIS_USER --github-token $TRAVIS_GHTOKEN
git clone --verbose --branch=develop git@github.com/F5Networks/f5-icontrol-rest-python.git /tmp
mv /tmp/f5-icontrol-rest-python/icontrol/ .

echo -e "Install complete";
