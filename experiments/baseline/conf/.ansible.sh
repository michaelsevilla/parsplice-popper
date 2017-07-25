#!/bin/bash

# These are the variables for running Ansible in a container
# If you know Ansible and Docker, the below should make sense
# - we attach ceph-ansible to root because they expect us to be in that dir
NETW="--net host -v $HOME/.ssh:/root/.ssh"
DIRS="-v `pwd`:/root"
ANSB="-w /root -v `pwd`/ansible/ansible.cfg:/etc/ansible/ansible.cfg"
CODE=""
WORK=""
ARGS="--forks 50"
VARS="-i conf/ansiblehosts -e @conf/vars.yml"
DOCKER="docker run -it --rm $NETW $DIRS $ANSB $CODE $WORK michaelsevilla/ansible $VARS"
