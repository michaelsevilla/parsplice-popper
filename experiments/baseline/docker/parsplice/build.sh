#!/bin/bash

# name of the final image
IMG="piha.soe.ucsc.edu:5000/parsplice"

# don't pull results on git lfs
export GIT_LFS_SKIP_SMUDGE=1

set -ex
if [ ! -d src ]; then
  git clone https://gitlab.com/mikesevilla3/parsplice.git src
  cd src; git checkout trinitite-uo2; cd -
fi

# setup by copying keys and source code (not deploy code)
cp -r ~/.ssh .

# launch a dev container
docker build -t $IMG .
set +ex
echo "DONE creating image named $IMG"
