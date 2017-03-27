#!/bin/bash

DIR="file://$( cd "$( dirname $( dirname $( dirname "${BASH_SOURCE[0]}" )))" && pwd )/docs/_build"
sphinx-build docs docs/_build
echo "Open ${DIR} in your browser"