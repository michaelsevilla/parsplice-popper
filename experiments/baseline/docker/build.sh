#!/bin/bash

# cleanup
rm -fr src /tmp/parsplice/ >> /dev/null 2>&1
mkdir src

# setup by copying keys and source code (not deploy code)
cp -r ~/.ssh .
for i in `ls ../../ | grep -v deploy`; do
  cp -r ../../$i src/$i
done

# launch a dev container
set -ex
docker build -t piha.soe.ucsc.edu:5000/parsplice .
