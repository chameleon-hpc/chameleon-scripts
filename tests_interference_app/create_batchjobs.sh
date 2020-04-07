#!/usr/local_rwth/bin/zsh

SB_ACCOUNT=jara0001
SB_PARTITION=c16m
SB_NUM_NODES=2
SB_TASKS_PER_NODE=1
SB_CPUS_PER_TASK=24
SB_EXEC_TIME_PER_RUN=01:00:00
SB_JOB_NAME_PREFIX=distrubance
SB_OUTPUT_PREFIX=sbatch
SB_EXTRA_ARGS=--exclusive

PATH_TO_MAIN_PROG=/work/jk869269/repos/disturbance/chameleon-apps/applications/
#PATH_TO_MAIN_PROG=~/repos/hpc/chameleon-apps/applications/

export SB_OMP_PLACES=cores
export SB_OMP_PROC_BIND=close

export CUR_DATE_STR="$(date +"%Y%m%d_%H%M%S")"

function run_sbatch {
    sbatch  --account=$SB_ACCOUNT \
            --partition=$SB_PARTITION \
            --nodes=$SB_NUM_NODES \
            --time=$SB_EXEC_TIME_PER_RUN \
            --ntasks-per-node=$SB_TASKS_PER_NODE \
            --cpus-per-task=${SB_CPUS_PER_TASK} \
            --job-name=${SB_OUTPUT_PREFIX}_${SB_NAME} \
            $SB_EXTRA_ARGS \
            --output=${SB_OUTPUT_PREFIX}_${SB_NAME}.txt \
            --export=SB_OMP_PLACES,SB_OMP_PROC_BIND,SB_OMP_NUM_THREADS,SB_DISTURB_RANKS,SB_PROG,SB_NAME,SB_DIST_TYPE,CUR_DATE_STR \
            run.sh
}

module use -a ~/.modules
module load chameleon-lib

# recreate fresh
export OUTPUT_DIR="${CUR_DATE_STR}_output-files"
export DIST_PID_FOLDER="${OUTPUT_DIR}/pid"
rm -rf ${OUTPUT_DIR}
rm *.txt
mkdir -p ${DIST_PID_FOLDER}

###########################################################################
#build
###########################################################################
make -C ${PATH_TO_MAIN_PROG}interference_app clean
make -C ${PATH_TO_MAIN_PROG}interference_app dist
#make -C ${PATH_TO_MAIN_PROG}interference_app trace
COMPILE_CHAMELEON=0 COMPILE_TASKING=1 PROG=tasking   ITERATIVE_VERSION=0 make -C ${PATH_TO_MAIN_PROG}matrix_example
COMPILE_CHAMELEON=1 COMPILE_TASKING=0 PROG=chameleon ITERATIVE_VERSION=0 make -C ${PATH_TO_MAIN_PROG}matrix_example

###########################################################################
#chameleon
###########################################################################

export SB_OMP_NUM_THREADS=23
export SB_PROG=chameleon

export SB_DISTURB_RANKS=0
export SB_NAME=chameleon_baseline
#run_sbatch

export SB_DISTURB_RANKS=1
export SB_DIST_TYPE=compute
export SB_NAME=chameleon_comp
run_sbatch

#export SB_DISTURB_RANKS=1
#export SB_DIST_TYPE=memory
#export SB_NAME=chameleon_mem
#run_sbatch

##########################################################################
#tasking
##########################################################################

export SB_OMP_NUM_THREADS=24
export SB_PROG=tasking

export SB_DISTURB_RANKS=0
export SB_NAME=tasking_baseline
#run_sbatch

export SB_DISTURB_RANKS=1
export SB_DIST_TYPE=compute
export SB_NAME=tasking_comp
run_sbatch

#export SB_DISTURB_RANKS=1
#export SB_DIST_TYPE=memory
#export SB_NAME=tasking_mem
#run_sbatch
