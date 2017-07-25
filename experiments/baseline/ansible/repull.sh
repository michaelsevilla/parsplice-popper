#!/bin/bash

set -ex
time ./run.sh mpiclient,mpiserver -m shell -a "docker pull piha.soe.ucsc.edu:5000/parsplice"
