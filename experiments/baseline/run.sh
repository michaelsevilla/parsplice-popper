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

# do a parameter sweep
for c in "t2000it400.xml" "t400it2000.xml" "t1000it2000.xml"; do

  # run the job
  ./teardown.sh
  ./setup.sh
  $DOCKER $ARGS -e config="$c" ansible/parsplice.yml ansible/collect.yml

  # grab configuration and save results
  cp conf/ps-config/$c results/ps-config.xml
  sleep 1
  mv results results-$c-scaletemp
done
exit 0
