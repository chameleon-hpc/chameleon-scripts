#!/bin/bash

ulimit -s unlimited
ulimit -c unlimited

export CUR_DATE_STR="$(date +"%Y%m%d_%H%M%S")"
# export CUR_OUTP_STR="${CUR_DATE_STR}_output"
export CUR_OUTP_STR="outputs/${TEST_NAME}/logs"

# export SAMOA_VTUNE_PREFIX=""

# export I_MPI_PIN=1
# export I_MPI_DEBUG=5
# export I_MPI_PIN_DOMAIN=auto
# export I_MPI_TMI_NBITS_RANK=16 #set env var for enabling larger tag size on OPA with IntelMPI and psm2

export ENVS_FOR_EXPORT="PATH,CPLUS_INCLUDE_PATH,C_INCLUDE_PATH,CPATH,INCLUDE,LD_LIBRARY_PATH,LIBRARY_PATH,OMP_NUM_THREADS,OMP_PLACES,OMP_PROC_BIND,MIN_ABS_LOAD_IMBALANCE_BEFORE_MIGRATION,CHAMELEON_TOOL_LIBRARIES,ENABLE_TRACE_FROM_SYNC_CYCLE,ENABLE_TRACE_TO_SYNC_CYCLE"
export SAMOA_PARAMS="-output_dir ${SAMOA_OUTPUT_DIR} -dmin ${DMIN} -dmax ${DMAX} -sections ${NUM_SECTIONS} ${ASAGI_PARAMS} ${SIM_LIMIT} "
# specific parameter set for ADER-DG-opt branch (e.g. Oscillating Lake)
# export SAMOA_PARAMS="-output_dir ${SAMOA_OUTPUT_DIR} -dmin ${DMIN} -dmax ${DMAX} -sections ${NUM_SECTIONS} ${ASAGI_PARAMS} ${SIM_LIMIT} -dry_dg_guard 0.01 -max_picard_error 10.0d-16 -max_picard_iterations 4 -courant 0.05 -drytolerance 0.000001 -coast_height_max -100000 -coast_height_min 100000"
