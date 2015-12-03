#!/bin/bash

echo "Building RedHat packages..."

cp -R /var/build /tmp
make -C /tmp/build rpms
cp -R /tmp/build/dist /var/build


