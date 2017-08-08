# DEPLOY

This guide uses Docker, Ansible, and CloudLab. If you are running on an HPC
system without these toolkits, you probably want to look at the
[INSTALL.md](INSTALL.md) guide so you can run ParSplice by hand.
[CloudLab](https://cloudlab.us/) is a service for researchers to check out
machines (both bare metal and virutal machines), free of charge. Using these
directions, you can set up ParSplice on CloudLab.

## Check Out Nodes

Using the [Docker MPI] Profile instantiate a cluster with at least 4 nodes on
CloudLab. That profile has Ubuntu images with Docker installed.  After you get
your nodes, you can use my convenience script to push your SSH keys:

[Docker MPI]: https://www.cloudlab.us/p/221d1125-6f4e-11e7-ac8f-90e2ba22fee4

```bash
wget https://raw.githubusercontent.com/michaelsevilla/parsplice-popper/cloudlab/experiments/baseline/cloudlab/pushkeys.sh
chmod 750 pushkeys.sh
vim pushkeys.sh
./pushkeys
```

## Grabbing Deploy Code

Log into the head node and setup git, and pull the code:

```bash
git config --global user.email "mikesevilla3@gmail.com"
git config --global user.name "Michael Sevilla"
git config --global core.editor "vim"
git clone https://github.com/michaelsevilla/parsplice-popper.git
cd parsplice-popper; git checkout cloudlab; git submodule update --init --recursive 
```

## Sanity Check the CloudLab Cluster

Make sure you can reach all nodes (i.e. your `./pushkeys.sh` invocation worked):

```bash
cd experiments/baseline/
vim conf/ansiblehosts
./run.sh all -m ping 
```

Also make sure that all NICs have the same names:

```bash
./run.sh all -m shell -a "ifconfig | grep eth2:0 -A1"
```

If some of your nodes do not have `eth2:0` defined, set the alias using the
commands from the CloudLab [install.sh](cloudlab/install/install.sh) script.

## Building a ParSplice Image
To avoid `apt-get` installing everything on all the nodes, we build a Docker
image and pull it from every node. This image will have all the source code and
binaries for ParSplice

```bash
cd experiments/baseline/docker
vim build.sh
```

Name your image and configure to push to your local repository, like so:

```diff
diff --git a/deploy/docker/build.sh b/deploy/docker/build.sh
index 540b0cc..bf2bb71 100755
--- a/deploy/docker/build.sh
+++ b/deploy/docker/build.sh
@@ -12,4 +12,4 @@ done
 
 # launch a dev container
 set -ex
-docker build -t piha.soe.ucsc.edu:5000/parsplice .
+docker build -t registry.gitlab.com/mikesevilla3/parsplice .
```

Then build your image and push it:

```bash
./build.sh
docker push registry.gitlab.com/mikesevilla3/parsplice
```

It should have you log in to the GitLab registry.

## Deploying the ParSplice Image on the CloudLab Cluster

Once your code is in the image sitting on the GitLab registry, have all nodes
pull the image. This script will pull a Docker image with Ansible, a scripting
language that basically does bash on multiple nodes:

```bash
cd experiments/baseline/ansible
DOCKER_PASSWORD=<YOUR PASSWORD> ./repull.sh
```

Next, modify your configurations:

```bash
cd ../conf
vim vars.yml
```

Also setup your LAMMPS configurations:

```bash
sed -i "s/<SocketsPerNode> 1 <\/SocketsPerNode>/<SocketsPerNode> 36 <\/SocketsPerNode>/g" ps-config/*
sed -i "s/<NWorkers> 1 <\/NWorkers>/<NWorkers> 2 <\/NWorkers>/g" ps-config/*
```

Finally, set up your MPI ranks and run!

```bash
SLURM_NODELIST=node-[0,1,2,3,4,5,6,7,8] python ../ansible/mkhosts-slurm-nospawn.py 1 30 1 1
cd ..
./run.sh
```

To make sure that your ParSplice is healthy, read the
[HEALTH.md](HEALTH.md) write-up.

## Collecting Results

All results will be in the working diretory of each node. The node running
`mpiserver` should have something like this:

```
$ ls  
CMakeCache.txt	Makefile     UOXeKr_zbl.eam.alloy  dbextract  input	    input.lammps.schottky  mpirun.out  parsplice  times.out	 traj.out
CMakeFiles	Splicer.chk  cmake_install.cmake   driver     input.lammps  mpirun.err		   out	       sub.slurm  times.out.chk  traj.out.chk
```

Where the `out` directory has all the logs. We want to tar this directory up on
each node and pull the results.
