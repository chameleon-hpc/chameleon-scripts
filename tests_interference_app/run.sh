#!/bin/zsh

export OMP_PLACES=${SB_OMP_PLACES:-cores}
export OMP_PROC_BIND=${SB_OMP_PROC_BIND:-spread}
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-24}
export DISTURB_RANKS=${SB_DISTURB_RANKS:-0}
export PROG=${SB_PROG:-main}
export NAME=${SB_NAME}

export DIST_NUM_THREADS=24
export DIST_TYPE=${SB_DIST_TYPE:-compute}
#export DIST_TYPE?=memory
#export DIST_TYPE?=communication
export DIST_RANDOM=false
#export DIST_RANDOM?=true
export DIST_COMP_WINDOW=10
export DIST_PAUSE_WINDOW=0
export DIST_MIN_COMP_WINDOW=2
export DIST_MAX_COMP_WINDOW=20
export DIST_RAM_MB=30000

module use -a ~/.modules
module load chameleon-lib
#mpiexec.hydra -np 4 -genvall ./wrapper.sh

for i in {0..30}
do
    export ITERATION_NUM=$i
    ${MPIEXEC} ${FLAGS_MPI_BATCH} ./wrapper.sh
done
