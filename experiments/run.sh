#!/bin/bash

set -ex

for job in "baseline" "baseline-nanoparticle"; do
  cd $job; ./run.sh; cd -
done
