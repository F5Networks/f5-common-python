#!/usr/bin/env bash

for l in 1 2 3 4 5 6 7 8 9 10
do
  vboxmanage startvm $BIGIP_NAME --type headless
  if [ $? -eq 0 ]; then
    break
  fi
  sleep 1
done