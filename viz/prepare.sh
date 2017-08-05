#!/bin/bash

if [ -z $1 ]; then
  echo "ERROR: Please provide the dir"
  exit 1
fi

DIR=$1
if [ ! -d "../$DIR" ]; then
  echo "ERROR: ../$DIR does not exist"
  exit 1
fi

rm -r tmp >> /dev/null 2>&1
set -e

DOCKER="docker run --rm -v `pwd`/tmp:/tmp"
for i in `seq 0 9`; do
  node="node-$i"

  tar xzf ../$DIR/${node}_utilization.tar.gz

  for metric in "user" "used"; do
    path=`find tmp -name ${metric}.wsp | grep ${node} | grep -v swap`
    $DOCKER --entrypoint=whisper-dump.py michaelsevilla/graphite $path > tmp/${node}.${metric}.out
    $DOCKER --entrypoint=sed             michaelsevilla/graphite -i "s/:/,/g" tmp/${node}.${metric}.out &
    echo "... done w/ $node metric=${metric}"
  done
done

done="false"
while [ "$done" == "false" ]; do
  ps ax | grep sed | grep docker | grep graphite >> /dev/null 2>&1
  if [ $? -ne 0 ]; then flag="true"; fi
  echo "... waiting for sed to finish"
  sleep 1
done
