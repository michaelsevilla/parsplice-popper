#!/bin/bash
# Put all your cleanup tasks here.
source conf/.ansible.sh
set -e

# prepare output directory
sudo rm -fr results || true
$DOCKER $ARGS ansible/cleanup.yml

exit 0
