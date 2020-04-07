#!/usr/local_rwth/bin/zsh
echo "$(date +"%Y%m%d_%H%M%S") - Rank ${PMI_RANK} - $(hostname) - Running wrapper_disturb_start"
DIST_PID_FILENAME=${DIST_PID_FOLDER}/${NAME}_${PMI_RANK}.pid

PATH_TO_DIST_PROG=/work/jk869269/repos/disturbance/chameleon-apps/applications/interference_app/
#PATH_TO_DIST_PROG=~/repos/hpc/chameleon-apps/applications/interference_app/

RANKS_TO_DISTURB=(1)

args="--type=${DIST_TYPE} --rank_number=${PMI_RANK} --window_us_comp=${DIST_WINDOW_US_COMP} --window_us_pause=${DIST_WINDOW_US_PAUSE} --use_multiple_cores=${DIST_NUM_THREADS} --use_random=${DIST_RANDOM} --window_us_size_min=${DIST_WINDOW_US_COMP_MIN} --window_us_size_max=${DIST_WINDOW_US_COMP_MAX} --use_ram=${DIST_RAM_MB}"
KMP_AFFINITY=verbose ${PATH_TO_DIST_PROG}dist.exe ${args} &> "${FILENAME}_dist_rank_${PMI_RANK}.txt" &
processID=$!

echo "$(date +"%Y%m%d_%H%M%S") - Rank ${PMI_RANK} - $(hostname) - will be disturbed with PID = ${processID} in process $$"
echo "${processID}" > "${DIST_PID_FILENAME}"
echo "$$" > "${DIST_PID_FILENAME}_shell"
sleep infinity