#!/bin/zsh

#PMI_RANK=1

#echo "Number of Ranks Requested $PMI_SIZE. Executing Rank $PMI_RANK, iteration num: $ITERATION_NUM"

export MATRIX_SIZE=300
export NUM_TASKS=1000
#kleinere größe, mehr tasks, zb 1000 tasks, size = 300
RANKS_TO_DISTURB=(1 3)

FILENAME=output-files/output_${NAME}_rank_${PMI_RANK}_${ITERATION_NUM}.txt
PATH_TO_MAIN_PROG=~/repos/hpc/chameleon-apps/applications/matrix_example/
PATH_TO_DIST_PROG=~/repos/hpc/chameleon-apps/applications/interference_app/

args="--type=$DIST_TYPE --rank_number=$PMI_RANK --use_multiple_cores=$DIST_NUM_THREADS --use_random=$DIST_RANDOM --window_size_min=$DIST_MIN_COMP_WINDOW --window_size_max=$DIST_MAX_COMP_WINDOW --use_ram=$DIST_RAM_MB"

echo "This is the Outputfile for Rank $PMI_RANK" >> $FILENAME

processID=""

if [[ 1 = $DISTURB_RANKS ]]; then
    for i in $RANKS_TO_DISTURB
    do
        if [[ $i = $PMI_RANK ]]; then
            ${PATH_TO_DIST_PROG}dist.exe ${args} >> $FILENAME &
            processID=$!
            echo "Rank $PMI_RANK will be disturbed with PID = $processID"
            echo "Disturbance PID is $processID" >> $FILENAME
            echo "Distrubance type is: $DIST_TYPE" >> $FILENAME
        fi
    done
fi
#${PATH_TO_MAIN_PROG}main $MATRIX_SIZE $NUM_TASKS $NUM_TASKS $NUM_TASKS $NUM_TASKS >> $FILENAME
${PATH_TO_MAIN_PROG}${PROG} $MATRIX_SIZE $NUM_TASKS $NUM_TASKS>> $FILENAME

if [[ 0 = $PMI_RANK ]]; then
    grep "Computations" $FILENAME
fi

if [[ $processID != "" ]]; then
    kill -9 $processID
fi