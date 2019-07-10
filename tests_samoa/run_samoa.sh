#!/bin/bash

#SBATCH --time 08:00:00
#SBATCH --exclusive
#SBATCH --account=jara0001
#SBATCH --partition=c16m

source ~/.bash_profile
module use ~/.modules

export I_MPI_PIN=1
export I_MPI_PIN_DOMAIN=auto
export OMP_PLACES=cores
export OMP_PROC_BIND=close

if [ "${REP_MODE}" = "0" ]; then
  export SUFFIX_RESULT_DIR="rep_0"
  module load chameleon/intel_rep_0 
elif [ "${REP_MODE}" = "1" ]; then
  export SUFFIX_RESULT_DIR="rep_1"
  module load chameleon/intel_rep_1
elif [ "${REP_MODE}" = "2" ]; then 
  export SUFFIX_RESULT_DIR="rep_2"
  module load chameleon/intel_rep_2
fi

DIR_RESULT="${OUTPUT_DIR_PRE}${CUR_DATE_STR}_results/${NPROCS}procs_${SUFFIX_RESULT_DIR}"
mkdir -p ${DIR_RESULT}
mkdir -p output

DMIN="${DMIN:-25}" 
DMAX="${DMAX:-25}" 
LBFREQ="${LBFREQ:-1}"
NMAX="${NMAX:-10}"
NTHREADS=(23)
#NTHREADS=(1 2 4 8 16)

NREPS="${NREPS:-1}"

SAMOA_PARAMS="${SAMOA_PARAMS:- -dmin ${DMIN} -dmax ${DMAX} -lbfreq ${LBFREQ} -nmax ${NMAX}}"

SAMOA_BIN="${SAMOA_BIN:-/home/ps659535/chameleon/samoa_chameleon/bin/samoa_swe_radial_dam_break_noasagi_chameleon}"

export MAX_TASKS_PER_RANK_TO_MIGRATE_AT_ONCE=1


echo "mpiexec -np ${NPROCS} ${SAMOA_BIN} ${SAMOA_PARAMS}"

function run_samoa()
{
  for r in `seq 1 ${NREPS}` 
  do 
     for t in "${NTHREADS[@]}"
     do
       export OMP_NUM_THREADS=${t}
       export MIN_REL_LOAD_IMBALANCE_BEFORE_MIGRATION=10000.0
       eval "mpiexec -np ${NPROCS} ${SAMOA_BIN} ${SAMOA_PARAMS}" &>  ${DIR_RESULT}/results_no_stealing_t${t}_r${r}${EXP_SUFFIX}.log
       export MIN_REL_LOAD_IMBALANCE_BEFORE_MIGRATION=0.10
       eval "mpiexec -np ${NPROCS} ${SAMOA_BIN} ${SAMOA_PARAMS}" &>  ${DIR_RESULT}/results_stealing_t${t}_r${r}${EXP_SUFFIX}.log
     done
  done
}

run_samoa
