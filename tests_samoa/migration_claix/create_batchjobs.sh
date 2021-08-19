#!/usr/local_rwth/bin/zsh

export VARS_EXPORT="DMIN,DMAX,RUN_RADIAL,RUN_OSCILL,RUN_ASAGI,RUN_TRACE,NUM_STEPS,ORIG_OMP_NUM_THREADS,SAMOA_DIR,SAMOA_OUTPUT_DIR,ASAGI_PARAMS,ENABLE_TRACE_FROM_SYNC_CYCLE,ENABLE_TRACE_TO_SYNC_CYCLE"
export NUM_STEPS=2000
export ORIG_OMP_NUM_THREADS=6
export RUN_TRACE=0
export ENABLE_TRACE_FROM_SYNC_CYCLE=1850
export ENABLE_TRACE_TO_SYNC_CYCLE=1950

# Run balanced radial dam break
export DMIN=18
export DMAX=18
export RUN_RADIAL=1
export RUN_OSCILL=0
export RUN_ASAGI=0
# sbatch --export=${VARS_EXPORT} ./samoa_chameleon_run_batch.sh

# Run imbalanced oscillating lake + asagi
export DMIN=18
export DMAX=25
export RUN_RADIAL=0
export RUN_OSCILL=0
export RUN_ASAGI=1
sbatch --export=${VARS_EXPORT} ./samoa_chameleon_run_batch.sh
