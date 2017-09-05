#!/bin/bash

set -x
jobs=`find . -type d -maxdepth 1 | grep scale`
for j in $jobs; do
  rm -rf scale-*/db0
  mv $j.out $j
  mv $j.err $j

  cd $j/out;
  mkdir perf;
  find . -type f -name 'perf.*' -maxdepth 1 -exec mv {} perf/ \;
  for i in `ls`; do
    tar czf $i.tar.gz $i
    rm -r $i
  done
  cd -

  cd $j
  tar czf times.tar.gz times.out
  tar czf traj.tar.gz traj.out
  rm -f times.out traj.out
  cd -
done
