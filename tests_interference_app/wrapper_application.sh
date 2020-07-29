#!/usr/local_rwth/bin/zsh

module use -a ~/.modules
module load chameleon-lib

echo "$(date +"%Y%m%d_%H%M%S") - Rank ${PMI_RANK} - $(hostname) - Running wrapper_application"

export MATRIX_SIZE=600
export NUM_TASKS=2000

#PATH_TO_MAIN_PROG=/work/jk869269/repos/disturbance/chameleon-apps/applications/matrix_example/
PATH_TO_MAIN_PROG=~/repos/hpc/chameleon-apps/applications/matrix_example/

# Chameleon threshold
export MIN_LOCAL_TASKS_IN_QUEUE_BEFORE_MIGRATION=${OMP_NUM_THREADS}
module load intelvtune


module load intelitac
mkdir -p trace_${VTUNE_NAME}_rank_${PMI_RANK}
export VT_LOGFILE_PREFIX=trace_${VTUNE_NAME}_rank_${PMI_RANK}

${PATH_TO_MAIN_PROG}${PROG} $MATRIX_SIZE $NUM_TASKS $NUM_TASKS #$NUM_TASKS $NUM_TASKS
#echo 0 > /proc/sys/kernel/perf_event_paranoid
#vtune -trace-mpi -result-dir ${VTUNE_NAME}_rank_${PMI_RANK} -collect hotspots -- ${PATH_TO_MAIN_PROG}${PROG} $MATRIX_SIZE $NUM_TASKS $NUM_TASKS

#mkdir ${VTUNE_NAME}_rank_${PMI_RANK}

#valgrind --tool=callgrind ${PATH_TO_MAIN_PROG}${PROG} $MATRIX_SIZE $NUM_TASKS $NUM_TASKS

#export app_processID=$!
#./monitor_mem.sh &> "${FILENAME}_base_rank_${PMI_RANK}_mem.txt"

echo "$(date +"%Y%m%d_%H%M%S") - Rank ${PMI_RANK} - $(hostname) - Finished wrapper_application"
