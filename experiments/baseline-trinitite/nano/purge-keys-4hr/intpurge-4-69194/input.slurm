#!/bin/bash
#
#SBATCH --time=04:10:00
#SBATCH --ntasks=32
#SBATCH --output /lustre/ttscratch1/%u/parsplice-output/nano/intpurge-4-%j.out
#SBATCH --error  /lustre/ttscratch1/%u/parsplice-output/nano/intpurge-4-%j.err
delay="100000"
nkeys="4"
job_dir="/lustre/ttscratch1/$USER/parsplice-output/nano/intpurge-${nkeys}-$SLURM_JOB_ID"
src_dir="/lustre/ttscratch1/$USER/parsplice-support"
bin_dir="/users/$USER/parsplice-install"
slurm="$src_dir/parsplice/sample-input/nanoparticle-growth/slurm/scale-purged-keys/parsplice-purge${nkeys}"

set -ex

# Setup: copy input templates and modify
mkdir -p $job_dir/out
cd $job_dir
for input in "input" "input.lammps" "voter-pt.eam"; do
  cp -r $src_dir/parsplice/sample-input/nanoparticle-growth/$input .
done
cp $slurm input.slurm
sed -i 's/<Delay> 1000000 <\/Delay>/<Delay> '"$delay"' <\/Delay>/g' input/*
sed -i 's/<MaxKeyUsage> -1 <\/MaxKeyUsage>/<MaxKeyUsage> '"$nkeys"' <\/MaxKeyUsage>/g' input/*

# Run ParSplice
$src_dir/parsplice/tools/mem.sh $job_dir/out/ &
python $src_dir/parsplice/node-affinity/mkhosts-slurm-nospawn.py 32 1 1 1
export LD_LIBRARY_PATH="$bin_dir/lib:$src_dir/boost_1_62_0/stage/lib"
#srun -n `wc -l layout | awk '{print $1}'` --out $job_dir/out/debug.log $bin_dir/parsplice
srun -n `wc -l layout | awk '{print $1}'` --output none $bin_dir/parsplice
