#!/usr/local_rwth/bin/zsh
# echo "Number of Ranks Requested $PMI_SIZE. Executing Rank $PMI_RANK"

module use -a ~/.modules
module load chameleon-lib

export MATRIX_SIZE=300
export NUM_TASKS=4000
#kleinere größe, mehr tasks, zb 1000 tasks, size = 300
RANKS_TO_DISTURB=(1)

#PATH_TO_MAIN_PROG=/work/jk869269/repos/disturbance/chameleon-apps/applications/matrix_example/
#PATH_TO_DIST_PROG=/work/jk869269/repos/disturbance/chameleon-apps/applications/interference_app/
PATH_TO_MAIN_PROG=~/repos/hpc/chameleon-apps/applications/matrix_example/
PATH_TO_DIST_PROG=~/repos/hpc/chameleon-apps/applications/interference_app/

args="--type=${DIST_TYPE} --rank_number=$PMI_RANK --window_us_comp=${DIST_WINDOW_US_COMP} --window_us_pause=${DIST_WINDOW_US_PAUSE} --use_multiple_cores=${DIST_NUM_THREADS} --use_random=${DIST_RANDOM} --window_us_size_min=${DIST_WINDOW_US_COMP_MIN} --window_us_size_max=${DIST_WINDOW_US_COMP_MAX} --use_ram=${DIST_RAM_MB}"
echo "Num Threads: ${OMP_NUM_THREADS}";
processID=""

if [[ "1" = "${DISTURB_RANKS}" ]]; then
    for i in in "${RANKS_TO_DISTURB[@]}"
    do
        if [[ $i = $PMI_RANK ]]; then
            KMP_AFFINITY=verbose ${PATH_TO_DIST_PROG}dist.exe ${args} &> "${FILENAME}_dist_rank_${PMI_RANK}.txt" &
            processID=$!
            echo "Rank $PMI_RANK will be disturbed with PID = $processID"
            echo "Disturbance PID is $processID"
            echo "Distrubance type is: ${DIST_TYPE}"
        fi
    done
fi

# Chameleon threshold
export MIN_LOCAL_TASKS_IN_QUEUE_BEFORE_MIGRATION=${OMP_NUM_THREADS}

#${PATH_TO_MAIN_PROG}main $MATRIX_SIZE $NUM_TASKS $NUM_TASKS $NUM_TASKS $NUM_TASKS
${PATH_TO_MAIN_PROG}${PROG} $MATRIX_SIZE $NUM_TASKS $NUM_TASKS

if [[ $processID != "" ]]; then
    echo "Rank $PMI_RANK : kill proc $processID"
    kill -9 $processID
fi