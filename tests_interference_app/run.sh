#!/usr/local_rwth/bin/zsh

export CUR_DATE_STR=${CUR_DATE_STR:-"$(date +"%Y%m%d_%H%M%S")"}

export OMP_PLACES=${SB_OMP_PLACES:-cores}
export OMP_PROC_BIND=${SB_OMP_PROC_BIND:-close}
export OMP_NUM_THREADS=${SB_OMP_NUM_THREADS:-24}
export DISTURB_RANKS=${SB_DISTURB_RANKS:-0}
export PROG=${SB_PROG:-main}
export NAME=${SB_NAME}

export DIST_NUM_THREADS=15 #${SB_OMP_NUM_THREADS:-23}
#export DIST_TYPE=${SB_DIST_TYPE:-compute}
export DIST_TYPE=${SB_DIST_TYPE:-memory}
#export DIST_TYPE=${SB_DIST_TYPE:-communication}
export DIST_RANDOM=false
#export DIST_RANDOM?=true
export DIST_WINDOW_US_COMP=300000
#export DIST_WINDOW_US_PAUSE=300000
export DIST_WINDOW_US_PAUSE=0
#export DIST_WINDOW_US_PAUSE=-1
export DIST_WINDOW_US_COMP_MIN=100000
export DIST_WINDOW_US_COMP_MAX=300000
export DIST_RAM_MB=30000
#export DIST_RAM_MB=1000
export DIST_COM_MODE=pingpong
#export DIST_COM_MODE=roundtrip
export DIST_COM_SIZE_MB=100

export OUTPUT_DIR="${CUR_DATE_STR}_output-files"
export DIST_PID_FOLDER="${OUTPUT_DIR}/pid"

export KMP_AFFINITY=verbose

#module load intelvtune

export SCOREP_EXPERIMENT_DIRECTORY=scorep_bt-mz_sum

for i in {0..0}
do
    export ITERATION_NUM=$i
    export FILENAME=${OUTPUT_DIR}/output_${NAME}_${ITERATION_NUM}
    export VTUNE_NAME=vtune_${NAME}_${ITERATION_NUM}
    if [[ "1" = "${DISTURB_RANKS}" ]]; then
        (${MPIEXEC} ${FLAGS_MPI_BATCH} --mem=30G --export=DIST_PID_FOLDER,FILENAME,NAME,OMP_PLACES,OMP_PROC_BIND,OMP_NUM_THREADS,DIST_NUM_THREADS,DIST_TYPE,DIST_WINDOW_US_COMP,DIST_WINDOW_US_PAUSE,DIST_WINDOW_US_COMP_MIN,DIST_WINDOW_US_COMP_MAX,DIST_RANDOM,DIST_RAM_MB,DIST_COM_MODE,DIST_COM_SIZE_MB,KMP_AFFINITY --oversubscribe -- ./wrapper_disturb_start.sh 2>&1 >> ${FILENAME}.txt &)
        
    fi
    ${MPIEXEC} ${FLAGS_MPI_BATCH} --mem=80G --export=ITERATION_NUM,OMP_PLACES,OMP_PROC_BIND,OMP_NUM_THREADS,PROG,NAME,DIST_NUM_THREADS,DIST_TYPE,DIST_WINDOW_US_COMP,DIST_WINDOW_US_PAUSE,DIST_WINDOW_US_COMP_MIN,DIST_WINDOW_US_COMP_MAX,DIST_RANDOM,DIST_RAM_MB,FILENAME,VTUNE_NAME,KMP_AFFINITY --oversubscribe ./wrapper_application.sh 2>&1 >> ${FILENAME}.txt

    #${MPIEXEC} ${FLAGS_MPI_BATCH} amplxe-cl -trace-mpi -result-dir vtune_results -collect threading ./wrapper_application.sh #2>&1 >> ${FILENAME}.txt

    #salloc srun --pty --mem-per-cpu=0 /bin/bash
    #./run_vtune_test.sh 2>&1 >> ${FILENAME}.txt

    if [[ "1" = "${DISTURB_RANKS}" ]]; then
        ${MPIEXEC} ${FLAGS_MPI_BATCH} --mem=100M --export=DIST_PID_FOLDER,FILENAME,NAME,OMP_PLACES,OMP_PROC_BIND,OMP_NUM_THREADS,DIST_NUM_THREADS,DIST_TYPE,DIST_WINDOW_US_COMP,DIST_WINDOW_US_PAUSE,DIST_WINDOW_US_COMP_MIN,DIST_WINDOW_US_COMP_MAX,DIST_RANDOM,DIST_RAM_MB,DIST_COM_MODE,DIST_COM_SIZE_MB,KMP_AFFINITY --oversubscribe -- ./wrapper_disturb_cleanup.sh 2>&1 >> ${FILENAME}.txt
    fi

    sleep 10
done
