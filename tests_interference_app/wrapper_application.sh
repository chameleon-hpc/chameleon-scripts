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

${PATH_TO_MAIN_PROG}${PROG} $MATRIX_SIZE $NUM_TASKS $NUM_TASKS $NUM_TASKS $NUM_TASKS
#${PATH_TO_MAIN_PROG}${PROG} $MATRIX_SIZE $NUM_TASKS $NUM_TASKS

echo "$(date +"%Y%m%d_%H%M%S") - Rank ${PMI_RANK} - $(hostname) - Finished wrapper_application"
