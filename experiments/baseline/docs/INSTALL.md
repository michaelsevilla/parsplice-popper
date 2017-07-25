# INSTALL

The ParSplice team did not have an install guide so I reverse engineered their
environment from the Docker image that they use for their continuous
integration pipeline, called [ubuntu-parsplice-latte-deps]. I created a new
Docker image based on Ubuntu Xenial; the resulting ParSplice [Dockerfile] can
be used as a dependency list and install guide for deployment on HPC systems.
Docker files are basically `bash` commands strung together to form images.

[ubuntu-parsplice-latte-deps]: https://gitlab.com/exaalt/parsplice/container_registry 
[Dockerfile]: https://gitlab.com/mikesevilla3/parsplice/blob/trinitite/deploy/docker/Dockerfile

## Compile

Assuming the ParSplice and LevelDB dependencies installed, you can compile
ParSplice. First get the version of ParSplice with my perfomance counters:

```bash
git clone https://gitlab.com/mikesevilla3/parsplice.git
cd parsplice
git checkout -b trinitite trinitite
```

Now you have to use a complicated cmake command to line up the dependencies. I
set up the enviroment variables to work for the Docker image using [Lines
94-101], so you will have to use something similar to the commands I use. 

[Lines 94-101]: https://gitlab.com/mikesevilla3/parsplice/blob/trinitite/deploy/docker/Dockerfile#L94

I added installation code (which is untested), so you should be able to use
`-DCMAKE_INSTALL_PREFIX}` to specify an install directory. Please edit [Lines
16-20] of the CMake file so we can build 4 binaries:

1. perf counters on
2. debug on
3. info on
4. none

[Lines 16-20]: https://gitlab.com/mikesevilla3/parsplice/blob/trinitite/CMakeLists.txt#L16

# RUNNING PARSPLICE
## Single Node

If you set up `/etc/mpihosts` with "localhost", you should be able to run
single node. First, copy the configuration filse to the working directory:

```bash
cp -r /parsplice/sample-input/UO2/* <INSTALL DIR>/
```

```bash
mpirun \
  --hostfile /etc/mpihosts \
  --output-filename out/p \
  -np 8 \
  ./parsplice
```

When I run out of Docker, I used the [run.sh](../run.sh) script.

## Multi Node

To run on multiple nodes, we use the [parsplice.pbs] script.  For more
information on deploying on multiple nodes with Docker, Ansible, and CloudLab,
please see [DEPLOY.md](DEPLOY.md).

[parsplice.pbs]: https://gitlab.com/mikesevilla3/parsplice/blob/trinitite/deploy/conf/parsplice.pbs

