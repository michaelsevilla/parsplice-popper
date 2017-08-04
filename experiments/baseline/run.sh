#!/bin/bash
# This file should contain the series of steps that are required to execute 
# the experiment. Any non-zero exit code will be interpreted as a failure
# by the 'popper check' command.
source conf/.ansible.sh
set -ex

# this script doubles as an Ansible commandline program
if [ ! -z $1 ]; then
  docker run -it --rm $NETW $DIRS $ANSB $CODE $WORK --entrypoint=ansible michaelsevilla/ansible $VARS "$@"
  exit
fi

# do a parameter sweep
mkdir results-parmsweep-keyspace || true
for c in "t1000it2000" "t400it2000" "t700it2000" "t2000it4000" "t400it4000" "t1200it4000"; do
  for run in 0; do

    # run the job
    ./teardown.sh
    ./setup.sh
    $DOCKER $ARGS -e config="${c}.xml" ansible/parsplice.yml ansible/collect.yml

    # grab configuration and save results
    cp conf/ps-config/${c}.xml results/ps-config.xml
    sleep 1
    mv results results-parmsweep-keyspace/$c-run$run
  done
done
exit 0
