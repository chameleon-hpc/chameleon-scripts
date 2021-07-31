#!/usr/local_rwth/bin/zsh

export CUR_DATE_STR=${CUR_DATE_STR:-"$(date +"%Y%m%d_%H%M%S")"}
export CUR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )" # get path of current script
# export OUT_DIR="${CUR_DIR}/outputs/output_"${CUR_DATE_STR}
export OUT_DIR="${CUR_DIR}/outputs/TopoMigrationCompare_S600_O1_"${CUR_DATE_STR}


TOOL_DIR=${CUR_DIR}/../../chameleon-apps/tools/tool_topo
# TOOL_DIR=${CUR_DIR}/../../chameleon-apps/tools/tool_sample
export CHAMELEON_TOOL_LIBRARIES="${TOOL_DIR}/tool.so"

export DIR_APPLICATION=${CUR_DIR}/../../chameleon-apps/applications/matrix_example


MY_EXPORTS="OUT_DIR,CUR_DATE_STR,MXM_PARAMS,CPUS_PER_TASK,MXM_SIZE,MXM_DISTRIBUTION,PROCS_PER_NODE,SOME_INDEX,NODES,CUR_DIR,CHAMELEON_TOOL_LIBRARIES,CHAMELEON_VERSION,DIR_APPLICATION"

#########################################################
#           Compile Chameleon Versions                  #
#########################################################
# cd ${CUR_DIR}/../../chameleon/src

# # Chameleon with my affinity extension
# export INSTALL_DIR=~/install/chameleon/intel
# make

# # chameleon with my affinity extension and keeping track of statistics
# export INSTALL_DIR=~/install/chameleon/intel_affinity_debug
# make aff_debug

# # Chameleon with my topology aware task migration tool and affinity extension
# export INSTALL_DIR=~/install/chameleon/intel_tool
# make tool

# # Chameleon with affinity extension but without comm thread
# export INSTALL_DIR=~/install/chameleon/intel_aff_no_commthread
# make aff_no_commthread

# # Chameleon without any of my modifications
# export INSTALL_DIR=~/install/chameleon/intel_no_affinity
# make vanilla

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
function chooseNodes()
{
    # x,y,... = x nodes under one leaf switch, x and y have to be on different leaf switches
    # WANTED_NODES="1,1"
    echo "Wanted nodes: ${WANTED_NODES}\n"
    python chooseNodes.py ${WANTED_NODES}
    source ${CUR_DIR}/chosenNodes.sh
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

###################### 1 Node ###########################
# export MXM_SIZE=600
# export MXM_DISTRIBUTION="1200"
# export CPUS_PER_TASK=48
# sbatch --nodes=1 --nodelist=${NODELIST} --ntasks-per-node=1 --cpus-per-task=${CPUS_PER_TASK} --job-name=mxm_affinity_testing \
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

###################### 4 Nodes ##########################
# export WANTED_NODES="2,1,1"
# chooseNodes
# export MXM_SIZE=600
# export MXM_DISTRIBUTION="300 300 300 300"
# export CPUS_PER_TASK=48
# sbatch --nodes=4 --nodelist=${NODELIST} --ntasks-per-node=1 --cpus-per-task=${CPUS_PER_TASK} --job-name=mxm_affinity_testing \
# --output=${OUT_DIR}/slurmOutput.txt \
# --export=${MY_EXPORTS} \
# run_experiments.sh

###################### 4 Nodes ##########################
export WANTED_NODES="3,3"
chooseNodes
export MXM_SIZE=600
export MXM_DISTRIBUTION=\
"2000 1000 500 0 "\
"2000 1000 500 0 "\
"2000 1000 500 0 "\
"2000 1000 500 0 "\
"2000 1000 500 0 "\
"2000 1000 500 0"
# export MXM_SIZE=90
# export MXM_DISTRIBUTION=\
# "20000 10000 5000 0 "\
# "20000 10000 5000 0 "\
# "20000 10000 5000 0 "\
# "20000 10000 5000 0 "\
# "20000 10000 5000 0 "\
# "20000 10000 5000 0"
export CPUS_PER_TASK=12
sbatch --nodes=6 --nodelist=${NODELIST} --ntasks-per-node=4 --cpus-per-task=${CPUS_PER_TASK} --job-name=mxm_topo_testing \
--output=${OUT_DIR}/slurmOutput.txt \
--export=${MY_EXPORTS} \
run_experiments.sh

################# 1 node, many ranks #####################
# export MXM_SIZE=300
# export MXM_DISTRIBUTION="300 300 300 300 300 300 300 300"
# export CPUS_PER_TASK=6
# sbatch --nodes=1 --ntasks-per-node=8 --cpus-per-task=${CPUS_PER_TASK} --job-name=mxm_affinity_testing \
# --output=${OUT_DIR}/slurmOutput.txt \
# --export=${MY_EXPORTS} \
# run_experiments.sh