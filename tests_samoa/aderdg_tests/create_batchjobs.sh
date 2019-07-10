#!/bin/bash

export CUR_DATE_STR="$(date +"%Y%m%d_%H%M%S")" 
DIR_CH_SRC=${DIR_CH_SRC:-~/chameleon/chameleon-lib/src}

make clean -C ${DIR_CH_SRC}
TARGET=claix_intel CUSTOM_COMPILE_FLAGS="-DCHAM_REPLICATION_MODE=0 -DCHAM_STATS_PER_SYNC_INTERVAL" INSTALL_DIR=~/chameleon/chameleon-lib/intel_1.0_rep_mode_0 make -C ${DIR_CH_SRC}

make clean -C ${DIR_CH_SRC}
TARGET=claix_intel CUSTOM_COMPILE_FLAGS="-DCHAM_REPLICATION_MODE=1 -DCHAM_STATS_PER_SYNC_INTERVAL" INSTALL_DIR=~/chameleon/chameleon-lib/intel_1.0_rep_mode_1 make -C ${DIR_CH_SRC}

make clean -C ${DIR_CH_SRC}
TARGET=claix_intel CUSTOM_COMPILE_FLAGS="-DCHAM_REPLICATION_MODE=2 -DCHAM_STATS_PER_SYNC_INTERVAL" INSTALL_DIR=~/chameleon/chameleon-lib/intel_1.0_rep_mode_2 make -C ${DIR_CH_SRC}

MODE=(0)
PROCS=(1 2 4 8 16 32)

export SAMOA_BIN="/home/ps659535/chameleon/samoa_chameleon/bin/samoa_1_unlimited"
export SAMOA_PARAMS="-courant 0.1  -dmin 15 -dmax 15 -tmax 0.5  -drytolerance 0.0000010 -coastheight 0.00025 -sections 16 "

export OUTPUT_DIR_PRE="/work/ps659535/aderdg_tests/"

for p in "${PROCS[@]}"
do

for m in "${MODE[@]}"
do 
  export REP_MODE=$m

  export NPROCS=$p
  sbatch --nodes=$p --ntasks-per-node=1 --cpus-per-task=24 --job-name=samoa_aderdg_rep${m}_${p}n --output=samoa_aderdg_rep${m}_${p}n.%J.txt --export=OUTPUT_DIR_PRE,SAMOA_BIN,SAMOA_PARAMS,REP_MODE,CUR_DATE_STR,NPROCS ../run_samoa.sh 

done

done
