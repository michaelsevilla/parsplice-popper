#!/bin/bash

set -ex
DPULL="docker pull piha.soe.ucsc.edu:5000/parsplice:nospawn"
cd .. 
time ./run.sh --forks 50  mpiclient,mpiserver -m shell -a "$DPULL"
