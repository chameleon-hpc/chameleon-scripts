#!/usr/local_rwth/bin/zsh


# parentPID=$(cat ${DIST_PID_FILENAME})
# childPID=$(pgrep -P $parentPID)
# echo "child $childPID"

echo "$(date +"%Y%m%d_%H%M%S") - Rank ${PMI_RANK} - $(hostname) - Running wrapper_disturb_cleanup"
DIST_PID_FILENAME=${DIST_PID_FOLDER}/${NAME}_${PMI_RANK}.pid

echo "$(date +"%Y%m%d_%H%M%S") - Rank ${PMI_RANK} - $(hostname) - Killing Disturb PID $(cat ${DIST_PID_FILENAME})"
#kill -9 $(cat ${DIST_PID_FILENAME}) 
kill -2 $(cat ${DIST_PID_FILENAME}) # required for regular program termination (e.g. if traces should be created)
sleep 5

echo "$(date +"%Y%m%d_%H%M%S") - Rank ${PMI_RANK} - $(hostname) - Killing Shell PID $(cat ${DIST_PID_FILENAME}_shell)"
kill -9 $(cat ${DIST_PID_FILENAME}_shell)

