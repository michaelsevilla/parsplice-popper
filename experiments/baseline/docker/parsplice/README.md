# Docker

There are a couple helper scripts in here:

- build.sh: builds an image with the source code in `../../`
- dev.sh: launches a development container, where we can compile and launch mpi with pbs
- conf/: used by the Docker image

## Quickstart

To run this, launch a developer container:

```bash
./dev.sh
```

Start the job:

```bash
qsub /tmp/parsplice.pbs
qrun 0
qstat
```
