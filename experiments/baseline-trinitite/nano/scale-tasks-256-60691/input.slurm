#!/bin/bash
#
#SBATCH --time=01:10:00
#SBATCH --nodes=8 --ntasks-per-node=32
#SBATCH --output /lustre/ttscratch1/%u/parsplice-output/nano/scale-tasks-256-%j.out
#SBATCH --error  /lustre/ttscratch1/%u/parsplice-output/nano/scale-tasks-256-%j.err
job_dir="/lustre/ttscratch1/$USER/parsplice-output/nano/scale-tasks-256-$SLURM_JOB_ID"
src_dir="/lustre/ttscratch1/$USER/parsplice-support"
bin_dir="/users/$USER/parsplice-install"
slurm="$src_dir/parsplice/sample-input/nanoparticle-growth/slurm/scale-workers/parsplice-t256"

set -ex

# Setup: copy input templates and modify
mkdir -p $job_dir/out
cd $job_dir
for input in "input" "input.lammps" "voter-pt.eam"; do
  cp -r $src_dir/parsplice/sample-input/nanoparticle-growth/$input .
done
cp $slurm input.slurm

# Run ParSplice
python $src_dir/parsplice/node-affinity/mkhosts-slurm-nospawn.py 32 1 1 1
export LD_LIBRARY_PATH="$bin_dir/lib:$src_dir/boost_1_62_0/stage/lib"
srun -n `wc -l layout | awk '{print $1}'` --output none $bin_dir/parsplice
