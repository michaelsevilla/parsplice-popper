#!/bin/bash
# This file should contain the series of steps that are required to execute 
# the experiment. Any non-zero exit code will be interpreted as a failure
# by the 'popper check' command.
source conf/.ansible.sh
set -e

# this script doubles as an Ansible commandline program
if [ ! -z $1 ]; then
  docker run -it --rm $NETW $DIRS $ANSB $CODE $WORK --entrypoint=ansible michaelsevilla/ansible $VARS "$@"
  exit
fi

# do a repeatability sweep
for i in `seq 0 2`; do
  for c in "nano.xml"; do
  
    ./teardown.sh
    ./setup.sh
  
    # run the actual job
    $DOCKER $ARGS -e config="$c" ansible/parsplice.yml ansible/collect.yml
    mv results results-$c-run$i-rerun
  done
done
exit 0
