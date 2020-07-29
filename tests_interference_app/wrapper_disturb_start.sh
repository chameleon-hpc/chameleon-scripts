#!/usr/local_rwth/bin/zsh

echo "$(date +"%Y%m%d_%H%M%S") - Rank ${PMI_RANK} - $(hostname) - Running wrapper_disturb_start"
DIST_PID_FILENAME=${DIST_PID_FOLDER}/${NAME}_${PMI_RANK}.pid

#PATH_TO_DIST_PROG=/work/jk869269/repos/disturbance/chameleon-apps/applications/interference_app/
export PATH_TO_DIST_PROG=~/repos/hpc/chameleon-apps/applications/interference_app/

#RANKS_TO_DISTURB=1,3
RANKS_TO_DISTURB=1
#export DEBUG=1

export args="--type=${DIST_TYPE} --rank_number=${PMI_RANK} --window_us_comp=${DIST_WINDOW_US_COMP} --window_us_pause=${DIST_WINDOW_US_PAUSE} --use_multiple_cores=${DIST_NUM_THREADS} --use_random=${DIST_RANDOM} --window_us_size_min=${DIST_WINDOW_US_COMP_MIN} --window_us_size_max=${DIST_WINDOW_US_COMP_MAX} --disturb_mem_mb_size=${DIST_RAM_MB} --com_type=${DIST_COM_MODE} --disturb_com_mb_size=${DIST_COM_SIZE} --ranks_to_disturb=${RANKS_TO_DISTURB}"


#KMP_AFFINITY=verbose valgrind --tool=memcheck --log-file=verbose_${DIST_TYPE}_dist_rank_${PMI_RANK}.txt ${PATH_TO_DIST_PROG}dist.exe ${args} &> "${FILENAME}_dist_rank_${PMI_RANK}.txt" &
#time KMP_AFFINITY=verbose ${PATH_TO_DIST_PROG}dist.exe ${args} &> "${FILENAME}_dist_rank_${PMI_RANK}.txt" &
KMP_AFFINITY=verbose ${PATH_TO_DIST_PROG}dist.exe ${args} &> "${FILENAME}_dist_rank_${PMI_RANK}.txt" &

#export timepid=$!
#echo "time pid = $timepid"
#export processID=$(pgrep -P $timepid)
#echo "dist pid = $processID"
export processID=$!
#export processID=$(ps --ppid ${processID} -o pid=)


echo "$(date +"%Y%m%d_%H%M%S") - Rank ${PMI_RANK} - $(hostname) - will be disturbed with PID = ${processID} in process $$"
#ps --ppid ${processID} -o pid= &> ${DIST_PID_FILENAME}_child
echo "${processID}" > "${DIST_PID_FILENAME}"
echo "$$" > "${DIST_PID_FILENAME}_shell"

#sleep 60
#echo "$(date +"%Y%m%d_%H%M%S") killed "
#echo "${pgrep -ns ${processID}}"
sleep infinity


# export app_processID=${processID}
# ./monitor_mem.sh &> "${FILENAME}_dist_rank_${PMI_RANK}_mem.txt"