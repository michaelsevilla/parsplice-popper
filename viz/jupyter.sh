#!/bin/bash

set -e -x
cd ../
docker run --rm -v `pwd`:/home/jovyan/work -p 81:8888 jupyter/scipy-notebook
