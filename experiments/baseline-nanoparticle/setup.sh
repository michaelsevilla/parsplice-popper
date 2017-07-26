#!/bin/bash
# Any setup required by the experiment goes here. Things like installing
# packages, allocating resources or deploying software on remote
# infrastructure can be implemented here.
source conf/.ansible.sh
set -e

mkdir results
for h in `cat conf/mpihosts | awk '{print $1}'`; do
  mkdir results/$h
done

$DOCKER $ARGS ansible/monitor.yml

exit 0
