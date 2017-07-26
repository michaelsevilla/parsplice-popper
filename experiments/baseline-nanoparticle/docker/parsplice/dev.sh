#!/bin/bash

# cleanup
docker stop parsplice-dev              >> /dev/null 2>&1
docker rm parsplice-dev                >> /dev/null 2>&1
rm /tmp/parsplice/build/parsplice.pbs* >> /dev/null 2>&1
set -ex

# start a container where we can run make and launch mpi
docker run -dit \
  --name parsplice-dev \
  --privileged \
  --net host \
  -v `pwd`/src:/parsplice \
  -e COMPILER="mpic++" \
  -e local_PREFIX="/usr/local/" \
  -e super_PREFIX="/usr/" \
  -e bldir_PREFIX="/builds/exaalt/parsplice/build/" \
  -e latte_PATH="/usr/local/LATTE" \
  -e RANK0=1 \
  -e PATH="$PATH:/parsplice/" \
  -v `pwd`/configure.sh:/usr/bin/configure.sh \
  -v `pwd`/parsplice.pbs:/tmp/parsplice.pbs \
  -v `pwd`/mpihosts:/tmp/mpihosts \
  -w "/root/" \
  piha.soe.ucsc.edu:5000/parsplice

# setup configuration
docker exec -it parsplice-dev /bin/bash -c "cp -r /parsplice/sample-input/UO2/* /root/"

# drop user into container
docker exec -it parsplice-dev /bin/bash
