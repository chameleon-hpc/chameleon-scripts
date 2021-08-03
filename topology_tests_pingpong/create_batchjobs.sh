#!/usr/local_rwth/bin/zsh

export CUR_DATE_STR=${CUR_DATE_STR:-"$(date +"%Y%m%d_%H%M%S")"}
export CUR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )" # get path of current script
export OUT_DIR="${CUR_DIR}/outputs/output_"${CUR_DATE_STR}
# export OUT_DIR="${CUR_DIR}/outputs/stats_mapMode_CheckPhy_NoNuma_1Node_PageChangeCheck"

TOOL_DIR=${CUR_DIR}/../../chameleon-apps/tools/tool_topo
# TOOL_DIR=${CUR_DIR}/../../chameleon-apps/tools/tool_sample
export CHAMELEON_TOOL_LIBRARIES="${TOOL_DIR}/tool.so"

export DIR_APPLICATION=${CUR_DIR}/../../chameleon-apps/applications/pingpong


MY_EXPORTS="OUT_DIR,CUR_DATE_STR,MXM_PARAMS,CPUS_PER_TASK,MXM_SIZE,MXM_DISTRIBUTION,PROCS_PER_NODE,SOME_INDEX,NODES,CUR_DIR,CHAMELEON_TOOL_LIBRARIES,CHAMELEON_VERSION,DIR_APPLICATION,REGION"

#########################################################
#           Compile Chameleon Versions                  #
#########################################################
# cd ${CUR_DIR}/../../chameleon/src

# export INSTALL_DIR=~/install/chameleon/intel_affinity_debug
# make aff_debug

# export INSTALL_DIR=~/install/chameleon/intel_no_affinity
# make vanilla

# export INSTALL_DIR=~/install/chameleon/intel_tool
# make tool

# export INSTALL_DIR=~/install/chameleon/intel
# make

# cd ${CUR_DIR}

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
#           Compile PingPong Benchmark                  #
#########################################################
cd ${CUR_DIR}/../../chameleon-apps/applications/pingpong
make
cd ${CUR_DIR}

#########################################################
#                   Choose nodes                        #
#########################################################
function chooseNodes()
{
    # x,y,... = x nodes under one leaf switch, x and y have to be on different leaf switches
    # WANTED_NODES="1,1"
    echo "Wanted nodes: ${WANTED_NODES}\n"
    python ../topology_tests/chooseNodes.py ${WANTED_NODES}
    source ${CUR_DIR}/../topology_tests/chosenNodes.sh
    if [ "${CHOOSE_NODES_FAILED}" -eq "1" ]
    then 
        echo "Failed to choose requested nodes!\n"
        exit 1 
    fi
    echo "NODELIST= $NODELIST \n"
}


#########################################################
#                       Tests                           #
#########################################################
mkdir -p ${OUT_DIR}

###################### 0 hops ##########################
export REGION=0
export WANTED_NODES="1"
chooseNodes
export CPUS_PER_TASK=24
sbatch --nodes=1 --nodelist=${NODELIST} --ntasks-per-node=2 --cpus-per-task=${CPUS_PER_TASK} --job-name=0_pingpong \
--output=${OUT_DIR}/slurmOutput.txt \
--export=${MY_EXPORTS} \
run_experiments.sh

###################### 2 hops ##########################
# export REGION=1
# export WANTED_NODES="2"
# chooseNodes
# export CPUS_PER_TASK=24
# sbatch --nodes=2 --nodelist=${NODELIST} --ntasks-per-node=1 --cpus-per-task=${CPUS_PER_TASK} --job-name=2_pingpong \
# --output=${OUT_DIR}/slurmOutput.txt \
# --export=${MY_EXPORTS} \
# run_experiments.sh

###################### 4 hops ##########################
# export REGION=2
# export WANTED_NODES="1,1"
# chooseNodes
# export CPUS_PER_TASK=24
# sbatch --nodes=2 --nodelist=${NODELIST} --ntasks-per-node=1 --cpus-per-task=${CPUS_PER_TASK} --job-name=4_pingpong \
# --output=${OUT_DIR}/slurmOutput.txt \
# --export=${MY_EXPORTS} \
# run_experiments.sh

# export CPUS_PER_TASK=48
# sbatch --nodes=2 --ntasks-per-node=1 --cpus-per-task=${CPUS_PER_TASK} --job-name=pingpong \
# --output=${OUT_DIR}/slurmOutput.txt \
# --export=${MY_EXPORTS} \
# run_experiments.sh