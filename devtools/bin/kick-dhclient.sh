#!/usr/bin/env bash

set +e
python ./devtools/bin/kick-dhclient.py --vmname $BIGIP_NAME
for l in 1 2 3 4 5 6 7 8 9 10
do
  curl -k -u admin:admin 'https://localhost:${BIGIP_PORT}/mgmt/tm/sys/db/failover.linksup' | jq -e '.value == "true"'
  if [ $? -eq 0 ]; then
    break
  fi
  sleep 1
done
set -e