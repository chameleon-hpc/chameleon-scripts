#!/bin/bash

export CUR_DATE_STR="$(date +"%Y%m%d_%H%M%S")" 
DIR_CH_SRC=${DIR_CH_SRC:-~/chameleon/chameleon-lib/src}

make clean -C ${DIR_CH_SRC}
TARGET=claix_intel CUSTOM_COMPILE_FLAGS="-DCHAM_REPLICATION_MODE=0 " INSTALL_DIR=~/chameleon/chameleon-lib/intel_1.0_rep_mode_0 make -C ${DIR_CH_SRC}

make clean -C ${DIR_CH_SRC}
TARGET=claix_intel CUSTOM_COMPILE_FLAGS="-DCHAM_REPLICATION_MODE=1 " INSTALL_DIR=~/chameleon/chameleon-lib/intel_1.0_rep_mode_1 make -C ${DIR_CH_SRC}

make clean -C ${DIR_CH_SRC}
TARGET=claix_intel CUSTOM_COMPILE_FLAGS="-DCHAM_REPLICATION_MODE=2 " INSTALL_DIR=~/chameleon/chameleon-lib/intel_1.0_rep_mode_2 make -C ${DIR_CH_SRC}

MODE=(0 1 2)
PROCS=(1 2 4 8 16 32) 

export NMAX=10
export NREPS=5

for p in "${PROCS[@]}"
do

for m in "${MODE[@]}"
do 
  export REP_MODE=$m

  export NPROCS=$p
  sbatch --nodes=$p --ntasks-per-node=1 --cpus-per-task=24 --job-name=samoa_rep${m}_${p}n --output=samoa_rep${m}_${p}n.%J.txt --export=NMAX,NREPS,REP_MODE,CUR_DATE_STR,NPROCS ../run_samoa.sh 
done

done
