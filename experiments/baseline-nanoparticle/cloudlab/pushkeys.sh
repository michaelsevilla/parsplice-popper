#!/bin/bash

set -e

for i in "c220g1-031104.wisc.cloudlab.us" \
         "c220g1-031107.wisc.cloudlab.us" \
         "c220g1-031111.wisc.cloudlab.us" \
         "c220g1-031106.wisc.cloudlab.us" \
         "c220g1-031115.wisc.cloudlab.us" \
         "c220g1-031121.wisc.cloudlab.us" \
         "c220g1-031118.wisc.cloudlab.us" \
         "c220g1-031113.wisc.cloudlab.us" \
         "c220g1-031120.wisc.cloudlab.us"; do
  echo "---- " $i
  scp ~/.ssh/id_rsa.pub ${USER}@$i:~/.ssh/id_rsa.pub
  scp ~/.ssh/id_rsa ${USER}@$i:~/.ssh/id_rsa
  ssh ${USER}@$i "sudo usermod -aG docker ${USER}"
done
