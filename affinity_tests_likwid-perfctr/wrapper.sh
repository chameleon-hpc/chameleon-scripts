#!/usr/local_rwth/bin/zsh
if [ "${RUN_LIKWID}" = "1" ]; then
    module load likwid
    LIKW_EXT="likwid-perfctr -o ${TMP_NAME_RUN}_hwc_R${PMI_RANK}.csv -O -f -c N:0-$((OMP_NUM_THREADS-1)) -g L3CACHE"
fi

# remember current cpuset for process
CUR_CPUSET=$(cut -d':' -f2 <<< $(taskset -c -p $(echo $$)) | xargs)
# echo "${PMI_RANK}: CUR_CPUSET = ${CUR_CPUSET}"

if [ "${RUN_LIKWID}" = "1" ]; then
    echo "Command executed for rank ${PMI_RANK}: ${LIKW_EXT} taskset -c ${CUR_CPUSET} ${DIR_MXM_EXAMPLE}/${PROG} ${MXM_PARAMS}"
    ${NO_NUMA_BALANCING} ${LIKW_EXT} taskset -c ${CUR_CPUSET} ${DIR_MXM_EXAMPLE}/${PROG} ${MXM_PARAMS}
else
    echo "Command executed for rank ${PMI_RANK}: ${LIKW_EXT} ${DIR_MXM_EXAMPLE}/${PROG} ${MXM_PARAMS}"
    ${NO_NUMA_BALANCING} ${LIKW_EXT} ${DIR_MXM_EXAMPLE}/${PROG} ${MXM_PARAMS}
fi
