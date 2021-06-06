#!/usr/local_rwth/bin/zsh

export CHAM_AFF_TASK_SELECTION_STRAT=3
export CHAM_AFF_PAGE_SELECTION_STRAT=7
export CHAM_AFF_PAGE_WEIGHTING_STRAT=2
export CHAM_AFF_CONSIDER_TYPES=1
export CHAM_AFF_PAGE_SELECTION_N=3
export CHAM_AFF_TASK_SELECTION_N=8

export OMP_NUM_THREADS=47

export MXM_PARAMS="600 100 100 100 100"

export CHAMELEON_VERSION="chameleon/intel"
sbatch --nodes=4 --ntasks-per-node=1 --cpus-per-task=48 --job-name=affinity_mxm \
--output=mxm_affinity.%J.txt \
--export=CHAMELEON_VERSION,MXM_PARAMS,OMP_NUM_THREADS,\
CHAM_AFF_TASK_SELECTION_STRAT,CHAM_AFF_PAGE_SELECTION_STRAT,CHAM_AFF_PAGE_WEIGHTING_STRAT,CHAM_AFF_CONSIDER_TYPES,CHAM_AFF_PAGE_SELECTION_N,CHAM_AFF_TASK_SELECTION_N \
run_experiments.sh

export CHAMELEON_VERSION="chameleon/intel_no_affinity"
sbatch --nodes=4 --ntasks-per-node=1 --cpus-per-task=48 --job-name=no_affinity_mxm \
--output=mxm_no_affinity.%J.txt \
--export=CHAMELEON_VERSION,MXM_PARAMS,OMP_NUM_THREADS \
run_experiments.sh