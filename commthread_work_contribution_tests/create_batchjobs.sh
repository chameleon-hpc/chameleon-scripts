#!/usr/local_rwth/bin/zsh

export CUR_DATE_STR=${CUR_DATE_STR:-"$(date +"%Y%m%d_%H%M%S")"}
export CUR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )" # get path of current script

# export TEST_NAME="ContributionVariation_3Threads_Stats_${CUR_DATE_STR}"
# export TEST_NAME="NumThreads_${CUR_DATE_STR}"
# export TEST_NAME="ContributionThreadScaling_${CUR_DATE_STR}"
export TEST_NAME="ScenariosThreadScaling_${CUR_DATE_STR}"

export OUT_DIR="${CUR_DIR}/outputs/"${TEST_NAME}
# export OUT_DIR="${CUR_DIR}/outputs/stats_mapMode_CheckPhy_NoNuma_1Node_PageChangeCheck"
mkdir -p ${OUT_DIR}


MY_EXPORTS="OUT_DIR,CUR_DATE_STR,MXM_PARAMS,CPUS_PER_TASK,MXM_SIZE,MXM_DISTRIBUTION,PROCS_PER_NODE,SOME_INDEX,NODES,CUR_DIR,TEST_NAME"

#########################################################
#           Compile Chameleon Versions                  #
#########################################################
# cd ${CUR_DIR}/../../chameleon/src

# export INSTALL_DIR=~/install/chameleon/intel_no_affinity
# make vanilla

# export INSTALL_DIR=~/install/chameleon/intel
# make commthread_contribution
# cd ${CUR_DIR}

#########################################################
#           Compile Matrix Example Versions             #
#########################################################
# export CHAMELEON_VERSION="chameleon/intel"

# cd ${CUR_DIR}/../../chameleon-apps/applications/matrix_example
# source ~/.zshrc
# module load $CHAMELEON_VERSION

# export COMPILE_CHAMELEON=1
# export COMPILE_TASKING=0
# export PROG="mxm_chameleon"
# make

# export COMPILE_CHAMELEON=0
# export COMPILE_TASKING=1
# export PROG="mxm_tasking"
# make

# cd ${CUR_DIR}

#########################################################
#                       Tests                           #
#########################################################

###################### 1 Node ###########################
export MXM_SIZE=600
export MXM_DISTRIBUTION="800 400 200 0"
export CPUS_PER_TASK=12
export PROCS_PER_NODE=4
sbatch --nodes=1 --ntasks-per-node=${PROCS_PER_NODE} --cpus-per-task=${CPUS_PER_TASK} --job-name=mxm_commthread_workcontribution \
--output=${OUT_DIR}/slurmOutput.txt \
--export=${MY_EXPORTS} \
run_experiments.sh

# ###################### 2 Nodes ##########################
# export MXM_SIZE=600
# export MXM_DISTRIBUTION="1200 1200"
# export CPUS_PER_TASK=48
# sbatch --nodes=2 --ntasks-per-node=1 --cpus-per-task=${CPUS_PER_TASK} --job-name=mxm_affinity_testing \
# --output=${OUT_DIR}/slurmOutput.txt \
# --export=${MY_EXPORTS} \
# run_experiments.sh
