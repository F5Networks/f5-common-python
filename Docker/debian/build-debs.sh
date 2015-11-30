#!/bin/bash

echo "Building debian packages..."

cp -R /var/build /tmp
make -C /tmp/build debs
cp -R /tmp/build/deb_dist /var/build


