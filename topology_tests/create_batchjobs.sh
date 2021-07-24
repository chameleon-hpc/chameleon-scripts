#!/usr/local_rwth/bin/zsh

export CUR_DATE_STR=${CUR_DATE_STR:-"$(date +"%Y%m%d_%H%M%S")"}
export CUR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )" # get path of current script
export OUT_DIR="${CUR_DIR}/outputs/output_"${CUR_DATE_STR}
# export OUT_DIR="${CUR_DIR}/outputs/stats_mapMode_CheckPhy_NoNuma_1Node_PageChangeCheck"
mkdir -p ${OUT_DIR}

TOOL_DIR=${CUR_DIR}/../../chameleon-apps/tools/tool_topo
# TOOL_DIR=${CUR_DIR}/../../chameleon-apps/tools/tool_sample
export CHAMELEON_TOOL_LIBRARIES="${TOOL_DIR}/tool.so"


MY_EXPORTS="OUT_DIR,CUR_DATE_STR,MXM_PARAMS,CPUS_PER_TASK,MXM_SIZE,MXM_DISTRIBUTION,PROCS_PER_NODE,SOME_INDEX,NODES,CUR_DIR,CHAMELEON_TOOL_LIBRARIES,CHAMELEON_VERSION"

#########################################################
#           Compile Chameleon Versions                  #
#########################################################
cd ${CUR_DIR}/../../chameleon/src

# export INSTALL_DIR=~/install/chameleon/intel_affinity_debug
# make aff_debug

# export INSTALL_DIR=~/install/chameleon/intel_no_affinity
# make vanilla

# export INSTALL_DIR=~/install/chameleon/intel_tool
# make tool

# export INSTALL_DIR=~/install/chameleon/intel
# make

cd ${CUR_DIR}

#########################################################
#           Compile Chameleon Tools                     #
#########################################################

export CHAMELEON_VERSION="chameleon/intel_tool"
source ~/.zshrc
module load $CHAMELEON_VERSION

cd ${TOOL_DIR}
make
cd ${CUR_DIR}


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
#                   Choose nodes                        #
#########################################################
# x,y,... = x nodes under one leaf switch, x and y have to be on different leaf switches
# WANTED_NODES="1,1"
# python chooseNodes.py ${WANTED_NODES}
# source ${CUR_DIR}/chosenNodes.sh
# if [ "${CHOOSE_NODES_FAILED}" -eq "1" ]
# then 
#     echo "Failed to choose requested nodes!\n"
#     exit 1 
# fi
# echo "NODELIST= $NODELIST \n"


#########################################################
#                       Tests                           #
#########################################################

###################### 1 Node ###########################
# export MXM_SIZE=600
# export MXM_DISTRIBUTION="1200"
# export CPUS_PER_TASK=48
# sbatch --nodes=1 --nodelist=${NODELIST} --ntasks-per-node=1 --cpus-per-task=${CPUS_PER_TASK} --job-name=mxm_affinity_testing \
# --output=${OUT_DIR}/slurmOutput.txt \
# --export=${MY_EXPORTS} \
# run_experiments.sh

# export MXM_SIZE=600
# export MXM_DISTRIBUTION="1200"
# export CPUS_PER_TASK=48
# sbatch --nodes=1 --ntasks-per-node=1 --cpus-per-task=${CPUS_PER_TASK} --job-name=mxm_affinity_testing \
# --output=${OUT_DIR}/slurmOutput.txt \
# --export=${MY_EXPORTS} \
# run_experiments.sh

###################### 2 Nodes ##########################
# export MXM_SIZE=600
# export MXM_DISTRIBUTION="1200 1200"
# export CPUS_PER_TASK=48
# sbatch --nodes=2 --nodelist=${NODELIST} --ntasks-per-node=1 --cpus-per-task=${CPUS_PER_TASK} --job-name=mxm_affinity_testing \
# --output=${OUT_DIR}/slurmOutput.txt \
# --export=${MY_EXPORTS} \
# run_experiments.sh

export MXM_SIZE=600
export MXM_DISTRIBUTION="1200 1200"
export CPUS_PER_TASK=48
sbatch --nodes=2 --ntasks-per-node=1 --cpus-per-task=${CPUS_PER_TASK} --job-name=mxm_affinity_testing \
--output=${OUT_DIR}/slurmOutput.txt \
--export=${MY_EXPORTS} \
run_experiments.sh
