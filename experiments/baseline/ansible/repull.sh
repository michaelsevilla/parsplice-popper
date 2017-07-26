#!/bin/bash

set -ex
LOGIN="docker login --password $DOCKER_PASSWORD --username mikesevilla3 registry.gitlab.com"
DPULL="docker pull registry.gitlab.com/mikesevilla3/parsplice"
cd .. 
time ./run.sh --forks 50  mpiclient,mpiserver -m shell -a "$LOGIN && $DPULL"
