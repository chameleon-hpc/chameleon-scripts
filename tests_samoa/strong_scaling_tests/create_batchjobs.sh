#!/bin/bash

export CUR_DATE_STR="$(date +"%Y%m%d_%H%M%S")" 
DIR_CH=${DIR_CH:-~/chameleon/chameleon-lib/}

CUR_DIR=${pwd}

if [ "${BUILD_CHAM}" = "1" ]; then

cd ${DIR_CH}

make clean 
cmake -DCMAKE_INSTALL_PREFIX="~/chameleon/chameleon-lib/intel_1.0_rep_mode_0" -DCMAKE_CXX_FLAGS="-DCHAM_STATS_RECORD -DCHAM_STATS_PRINT -DCHAM_REPLICATION_MODE=0 " cmake .
make install

make clean 
cmake -DCMAKE_INSTALL_PREFIX="~/chameleon/chameleon-lib/intel_1.0_rep_mode_1" -DCMAKE_CXX_FLAGS="-DCHAM_STATS_RECORD -DCHAM_STATS_PRINT -DCHAM_REPLICATION_MODE=1 " cmake .
make install

make clean 
cmake -DCMAKE_INSTALL_PREFIX="~/chameleon/chameleon-lib/intel_1.0_rep_mode_2" -DCMAKE_CXX_FLAGS="-DCHAM_STATS_RECORD -DCHAM_STATS_PRINT -DCHAM_REPLICATION_MODE=2 " cmake .
make install

make clean 
cmake -DCMAKE_INSTALL_PREFIX="~/chameleon/chameleon-lib/intel_no_communication_thread" -DCMAKE_CXX_FLAGS="-DCHAM_STATS_RECORD -DCHAM_STATS_PRINT -DENABLE_COMM_THREAD=0 " cmake .
make install

make clean
cmake -DCMAKE_INSTALL_PREFIX="~/chameleon/chameleon-lib/intel_tool" -DCMAKE_CXX_FLAGS="-DCHAM_STATS_RECORD -DCHAM_STATS_PRINT -DCHAMELEON_TOOL_SUPPORT=1 -DCHAM_STATS_PER_SYNC_INTERVAL -DCHAM_REPLICATION_MODE=0 " cmake .
make install

cd ${CUR_DIR}

fi

SAMOA_DIR=/home/ps659535/chameleon/samoa_chameleon
SAMOA_PATCH_ORDER=7

module use /home/ps659535/.modules
module purge
module load DEVELOP
module load intel/19.0
module load intelmpi/2018
module load cmake/3.6.0
module load chameleon
module load python/3.6.0
module load intelitac/2019

CUR_DIR=$(pwd)
cd ${SAMOA_DIR}
module load git
git checkout master

if [ "${BUILD}" = "1" ]; then

# standard builds
scons asagi=off target=release scenario=swe swe_patch_order=${SAMOA_PATCH_ORDER} data_refinement=sample swe_scenario=radial_dam_break flux_solver=aug_riemann assertions=on compiler=intel -j8
scons asagi=off target=release scenario=swe swe_patch_order=${SAMOA_PATCH_ORDER} data_refinement=sample swe_scenario=oscillating_lake flux_solver=aug_riemann assertions=on compiler=intel -j8
scons asagi=on  target=release scenario=swe swe_patch_order=${SAMOA_PATCH_ORDER} data_refinement=sample flux_solver=aug_riemann assertions=on compiler=intel -j8

# standard build with packing/unpacking
scons asagi=off target=release scenario=swe swe_patch_order=${SAMOA_PATCH_ORDER} data_refinement=sample swe_scenario=radial_dam_break flux_solver=aug_riemann assertions=on compiler=intel chameleon=2 -j8
scons asagi=off target=release scenario=swe swe_patch_order=${SAMOA_PATCH_ORDER} data_refinement=sample swe_scenario=oscillating_lake flux_solver=aug_riemann assertions=on compiler=intel chameleon=2  -j8
scons asagi=on  target=release scenario=swe swe_patch_order=${SAMOA_PATCH_ORDER} data_refinement=sample flux_solver=aug_riemann assertions=on compiler=intel chameleon=2 -j8

# chameleon builds
scons asagi=off target=release scenario=swe swe_patch_order=${SAMOA_PATCH_ORDER} data_refinement=sample swe_scenario=radial_dam_break flux_solver=aug_riemann assertions=on compiler=intel chameleon=1 -j8
scons asagi=off target=release scenario=swe swe_patch_order=${SAMOA_PATCH_ORDER} data_refinement=sample swe_scenario=oscillating_lake flux_solver=aug_riemann assertions=on compiler=intel chameleon=1 -j8
scons asagi=on target=release scenario=swe swe_patch_order=${SAMOA_PATCH_ORDER} data_refinement=sample flux_solver=aug_riemann assertions=on compiler=intel chameleon=1 -j8

module unload chameleon
fi

cd ${CUR_DIR}

# ===== Tohoku Scenario =====
export TOHOKU_PARAMS="-fbath /home/ps659535/chameleon/samoa_chameleon/data/tohoku_static/bath.nc -fdispl /home/ps659535/chameleon/samoa_chameleon/data/tohoku_static/displ.nc"

# ===== Simulation Settings =====
export NUM_SECTIONS=16
export CUR_DMIN=15
export CUR_DMAX=25
export NUM_STEPS=150
export SIM_TIME_SEC=3600


export NREPS=1
export SAMOA_BIN="/home/ps659535/chameleon/samoa_chameleon/bin/samoa_swe_chameleon"
export SAMOA_PARAMS=" -lbfreq 1000000 -dmin ${CUR_DMIN} -dmax ${CUR_DMAX} -sections ${NUM_SECTIONS} -tmax ${SIM_TIME_SEC} ${TOHOKU_PARAMS}"
export MODE=(3)
export PROCS=(1 2 4 8 16 32)

export EXP_SUFFIX="_chameleon_tool_strong"

export EXPORTS="SAMOA_BIN,SAMOA_PARAMS,NREPS,REP_MODE,CUR_DATE_STR,NPROCS,EXP_SUFFIX"

for p in "${PROCS[@]}"
do

for m in "${MODE[@]}"
do 
  export REP_MODE=$m
  export NPROCS=${p}
  sbatch --nodes=${p} --ntasks-per-node=1 --cpus-per-task=24 --job-name=samoa_strongrep${m}_${p}n --output=samoa_strong_rep${m}_${p}n.%J.txt --export="${EXPORTS}" ../run_samoa.sh 
done

done
