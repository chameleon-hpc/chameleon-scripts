#!/bin/bash
#SBATCH -J mxm_test_
#SBATCH -o mxm_%j.out
#SBATCH -e mxm_%j.err
#SBATCH -D ./
##SBATCH --mail-type=ALL
##SBATCH --mail-user=samfass@in.tum.de
#SBATCH --no-requeue
#SBATCH --account=pr48ma
#SBATCH --partition=test
#SBATCH --time=00:10:00
#SBATCH --nodes=2
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=48
#SBATCH --exclusive
#SBATCH --mem=MaxMemPerNode
#SBATCH --ear=off

source /etc/profile.d/modules.sh

module load slurm_setup
module switch python/3.6_intel
module switch mpi.intel/2019

module use ~/.modules
module load chameleon/intel_rep_4

#export MAX_PERCENTAGE_REPLICATED_TASKS=0.0
export MAX_PERCENTAGE_REPLICATED_TASKS=0.0
export MIN_ABS_LOAD_IMBALANCE_BEFORE_MIGRATION=2.000000
export MAX_TASKS_PER_RANK_TO_ACTIVATE_AT_ONCE=0
export PERCENTAGE_DIFF_TASKS_TO_MIGRATE=0.5

ulimit -s unlimited

mkdir -p output
export OMP_NUM_THREADS=2
#export OMP_NUM_THREADS=1

export VT_LOGFILE_NAME="main_00_rep0"

ldd /dss/dsshome1/02/di57zoh3/chameleon/chameleon-apps/applications/matrix_example/main

mpiexec ./wrapper_sudden_dist.sh 1.2 0 0  "/dss/dsshome1/02/di57zoh3/chameleon/chameleon-apps/applications/matrix_example/main" "150 100 100" 

echo "Done"



