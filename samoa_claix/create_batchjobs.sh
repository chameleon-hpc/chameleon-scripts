#!/usr/local_rwth/bin/zsh
export CUR_DATE_STR=${CUR_DATE_STR:-"$(date +"%Y%m%d_%H%M%S")"}
export CUR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )" # get path of current script

export TEST_NAME="Comparison_50Steps_4Threads_${CUR_DATE_STR}"

export SAMOA_DIR="/home/ka387454/repos/samoa-chameleon"
export SAMOA_OUTPUT_DIR="/home/ka387454/repos/chameleon-scripts/samoa_claix/outputs/${TEST_NAME}/samoa_out"
mkdir -p ${SAMOA_OUTPUT_DIR}

export OUT_DIR="${CUR_DIR}/outputs/${TEST_NAME}"
mkdir -p ${OUT_DIR}

export ASAGI_PARAMS="-fbath /home/ka387454/data/Tohoku/bath.nc -fdispl /home/ka387454/data/Tohoku/displ.nc"

export OLD_EXPORTS="DMIN,DMAX,RUN_RADIAL,RUN_OSCILL,RUN_ASAGI,RUN_TRACE,NUM_STEPS,ORIG_OMP_NUM_THREADS,SAMOA_DIR,SAMOA_OUTPUT_DIR,ASAGI_PARAMS,ENABLE_TRACE_FROM_SYNC_CYCLE,ENABLE_TRACE_TO_SYNC_CYCLE,"
export MY_EXPORTS="CUR_DIR,CUR_DATE_STR,TEST_NAME,CHAMELEON_VERSION"

#########################################################
#           Compile Chameleon Versions                  #
#########################################################
cd ${CUR_DIR}/../../chameleon/src

# #* Chameleon with my affinity extension
# export INSTALL_DIR=~/install/chameleon/intel
# make

# #* Chameleon without any of my modifications
# export INSTALL_DIR=~/install/chameleon/intel_no_affinity
# make vanilla

# #* chameleon with my affinity extension and keeping track of statistics
# export INSTALL_DIR=~/install/chameleon/intel_affinity_debug
# make aff_debug

# #* Chameleon with my topology aware task migration tool and affinity extension
# export INSTALL_DIR=~/install/chameleon/intel_tool
# make tool

# #* Chameleon with affinity extension but without comm thread
# export INSTALL_DIR=~/install/chameleon/intel_aff_no_commthread
# make aff_no_commthread

# # ! tracing tool
# module load intelitac
# export INSTALL_DIR=~/install/chameleon/intel_no_affinity
# CUSTOM_COMPILE_FLAGS="-DUSE_TASK_AFFINITY=0 -DCHAMELEON_TOOL_SUPPORT=0" make trace
# export INSTALL_DIR=~/install/chameleon/intel
# CUSTOM_COMPILE_FLAGS="-DUSE_TASK_AFFINITY=1 -DCHAMELEON_TOOL_SUPPORT=0" make trace

cd ${CUR_DIR}


export CHAMELEON_VERSION="chameleon/intel_no_affinity"

# export NUM_STEPS=2000
# export NUM_STEPS=150 #? How long is one simulated time step in reality?
export ORIG_OMP_NUM_THREADS=4 #? Do those change automatically over time? Why ORIG...?
export RUN_TRACE=0  #! Tracing
export ENABLE_TRACE_FROM_SYNC_CYCLE=1850
export ENABLE_TRACE_TO_SYNC_CYCLE=1950

# Run balanced radial dam break
export DMIN=18
export DMAX=18
export RUN_RADIAL=1
export RUN_OSCILL=0
export RUN_ASAGI=0
# sbatch --export=${VARS_EXPORT} ./samoa_chameleon_run_batch.sh

# Run imbalanced oscillating lake + asagi
export DMIN=18
export DMAX=25
export RUN_RADIAL=0
export RUN_OSCILL=0
export RUN_ASAGI=1
sbatch --nodes=2 --ntasks-per-node=1 --cpus-per-task=48 --job-name=samoa_chameleon \
--output=${OUT_DIR}/slurmOutput.txt \
--export=${OLD_EXPORTS}${MY_EXPORTS} \
${CUR_DIR}/samoa_chameleon_run_batch.sh