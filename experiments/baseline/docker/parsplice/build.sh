#!/bin/bash

#IMG="piha.soe.ucsc.edu:5000/parsplice"
IMG="registry.gitlab.com/mikesevilla3/parsplice"

set -ex

# setup by copying keys and source code (not deploy code)
if [ ! -d "src" ]; then
  git clone https://gitlab.com/mikesevilla3/parsplice.git src
  cd src; git checkout trinitite-nanoparticle; cd -
fi

# launch a dev container
cp -r ~/.ssh .
docker build -t $IMG .
set +x
echo -e "\nCreated $IMG\n"
