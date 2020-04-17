#!/bin/bash

export CUR_DATE_STR="$(date +"%Y%m%d_%H%M%S")" 
DIR_CH_SRC=${DIR_CH_SRC:-~/chameleon/chameleon-lib/}

CUR_DIR=$(pwd)

cd ${DIR_CH_SRC}

if [ "${BUILD_CHAM}" = "1" ]
then

make clean 
cmake -DCMAKE_INSTALL_PREFIX="~/chameleon/chameleon-lib/intel_1.0_rep_mode_0" -DCMAKE_CXX_FLAGS="-DCHAM_STATS_RECORD -DCHAM_STATS_PRINT -DCHAM_REPLICATION_MODE=0  " cmake .
make install

make clean 
cmake -DCMAKE_INSTALL_PREFIX="~/chameleon/chameleon-lib/intel_1.0_rep_mode_1" -DCMAKE_CXX_FLAGS="-DCHAM_STATS_RECORD -DCHAM_STATS_PRINT -DCHAM_REPLICATION_MODE=1 -DCHAM_STATS_PER_SYNC_INTERVAL " cmake .
make install

make clean 
cmake -DCMAKE_INSTALL_PREFIX="~/chameleon/chameleon-lib/intel_1.0_rep_mode_2" -DCMAKE_CXX_FLAGS="-DCHAM_STATS_RECORD -DCHAM_STATS_PRINT -DCHAM_REPLICATION_MODE=2 -DCHAM_STATS_PER_SYNC_INTERVAL " cmake .
make install

make clean 
cmake -DCMAKE_INSTALL_PREFIX="~/chameleon/chameleon-lib/intel_no_communication_thread" -DCMAKE_CXX_FLAGS="-DCHAM_STATS_RECORD -DCHAM_STATS_PRINT -DENABLE_COMM_THREAD=0 " cmake .
make install

make clean
cmake -DCMAKE_INSTALL_PREFIX="~/chameleon/chameleon-lib/intel_tool" -DCMAKE_CXX_FLAGS="-DCHAM_STATS_RECORD -DCHAM_STATS_PRINT -DCHAMELEON_TOOL_SUPPORT=1 -DCHAM_STATS_PER_SYNC_INTERVAL -DCHAM_REPLICATION_MODE=0 " cmake .
make install


fi

cd ${CUR_DIR}

MODE=(0)
PROCS=(1 2 4 8 16 32 64 128)

export SAMOA_BIN="/home/ps659535/chameleon/samoa_chameleon/bin/samoa_4_unlimited_cham_1"
#export SAMOA_PARAMS="-courant 0.1  -dmin 20 -dmax 20 -tmax 0.5  -drytolerance 0.0000010 -coastheight 0.00025 -sections 16 "
export SAMOA_PARAMS="-courant 0.1 -dmin 20 -dmax 20 -nmax 1000  -drytolerance 0.0000010 -coastheight 0.00025 -sections 16 "

#export NTHREADS=23
export OUTPUT_DIR_PRE="/work/ps659535/aderdg_tests/long_aderdg_stealing_t${NTHREADS}_"
export FILE_PRE="stealing"
#export NTHREADS=23

for p in "${PROCS[@]}"
do

for m in "${MODE[@]}"
do 
  export REP_MODE=$m
  echo $p,$NTHREADS
  export NPROCS=$p
  sbatch --nodes=$p --ntasks-per-node=1 --cpus-per-task=24 --job-name=samoa_aderdg_rep${m}_${p}n --output=samoa_aderdg_rep${m}_${p}n.%J.txt --export=OUTPUT_DIR_PRE,FILE_PRE,SAMOA_BIN,SAMOA_PARAMS,REP_MODE,CUR_DATE_STR,NPROCS,NTHREADS ../run_samoa.sh 

done

done
