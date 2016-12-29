#!/usr/bin/env bash

git --no-pager diff --name-only origin/development $GIT_COMMIT | egrep -v '(^requirements\.|^setup.py)' | egrep '(^f5\/iworkflow\/)' > pytest.iworkflow.jenkins.txt
git --no-pager diff --name-only origin/development $GIT_COMMIT | egrep -v '(^requirements\.|^setup.py)' | egrep '(^f5\/bigip\/)' > pytest.bigip.jenkins.txt
git --no-pager diff --name-only origin/development $GIT_COMMIT | egrep -v '(^requirements\.|^setup.py)' | egrep '(^f5\/bigiq\/)' > pytest.bigiq.jenkins.txt