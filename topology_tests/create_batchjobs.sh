#!/usr/local_rwth/bin/zsh

export CUR_DATE_STR=${CUR_DATE_STR:-"$(date +"%Y%m%d_%H%M%S")"}
export CUR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )" # get path of current script
# export OUT_DIR="${CUR_DIR}/outputs/output_"${CUR_DATE_STR}


TOOL_DIR=${CUR_DIR}/../../chameleon-apps/tools/tool_topo
# TOOL_DIR=${CUR_DIR}/../../chameleon-apps/tools/tool_sample
export CHAMELEON_TOOL_LIBRARIES="${TOOL_DIR}/tool.so"

export DIR_APPLICATION=${CUR_DIR}/../../chameleon-apps/applications/matrix_example


MY_EXPORTS="OUT_DIR,CUR_DATE_STR,MXM_PARAMS,CPUS_PER_TASK,MXM_SIZE,MXM_DISTRIBUTION,PROCS_PER_NODE,SOME_INDEX,NODES,CUR_DIR,CHAMELEON_TOOL_LIBRARIES,CHAMELEON_VERSION,DIR_APPLICATION,NODELIST,GROUP_INDEX,OUT_DIR_NAME"

#########################################################
#           Compile Chameleon Versions                  #
#########################################################
cd ${CUR_DIR}/../../chameleon/src

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

# ! tracing tool
module load intelitac
export INSTALL_DIR=~/install/chameleon/intel_tool
CUSTOM_COMPILE_FLAGS="-DUSE_TASK_AFFINITY=1 -DCHAMELEON_TOOL_SUPPORT=1" make trace

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
function chooseNodes()
{
    # x,y,... = x nodes under one leaf switch, x and y have to be on different leaf switches
    # WANTED_NODES="1,1"
    echo "Wanted nodes: ${WANTED_NODES}\n"
    python ${CUR_DIR}/chooseNodes.py ${WANTED_NODES}
    source ${CUR_DIR}/chosenNodes.sh
    # if [ "${CHOOSE_NODES_FAILED}" -eq "1" ]
    # then 
    #     echo "Failed to choose requested nodes!\n"
    #     exit 1 
    # fi
    echo "NODELIST= $NODELIST \n"
}


#########################################################
#                       Tests                           #
#########################################################
# export OUT_DIR="${CUR_DIR}/outputs/Topo_Ultimate_"${CUR_DATE_STR}
# mkdir -p ${OUT_DIR}
export GROUP_INDEX=-1

###################### 6 Nodes 4 PPN ##########################
for try in {1..120} # try multiple times when nodes are occupied
do
export OUT_DIR_NAME="Trace_NoAff_Topo_4PPN_S90_OLS0_OS1_0Hops_${CUR_DATE_STR}"
export OUT_DIR="${CUR_DIR}/outputs/${OUT_DIR_NAME}"
export WANTED_NODES="3,3"
chooseNodes
if [ "${CHOOSE_NODES_FAILED}" -eq "1" ]
then 
    echo "Failed to choose requested nodes!\nTry ${try}\nTrying again in 1 min.\n"
    sleep 60
    continue 
fi
mkdir -p ${OUT_DIR}
mkdir ${CUR_DIR}/Tracing/${OUT_DIR_NAME} && cd $_ #! Tracing
export CPUS_PER_TASK=12
export PROCS_PER_NODE=4
sbatch --nodes=6 --nodelist=${NODELIST} --ntasks-per-node=4 --cpus-per-task=${CPUS_PER_TASK} --job-name=4PPN_topo_mxm \
--output=${OUT_DIR}/slurmOutput4PPN.txt \
--export=${MY_EXPORTS} \
${CUR_DIR}/run_experiments.sh
break
done

###################### 6 Nodes 2 PPN ##########################
# for try in {1..120} # try multiple times when nodes are occupied
# do
# export OUT_DIR_NAME="Trace_NoAff_Topo_2PPN_S600_OLS1_0Hops_${CUR_DATE_STR}"
# # export OUT_DIR_NAME="Stats_NoAff_Topo_2PPN_S600_OLS1_${CUR_DATE_STR}"
# export OUT_DIR="${CUR_DIR}/outputs/${OUT_DIR_NAME}"
# mkdir -p ${OUT_DIR}
# # mkdir ${CUR_DIR}/Tracing/${OUT_DIR_NAME} && cd $_ #! Tracing
# export WANTED_NODES="3,3"
# chooseNodes
# if [ "${CHOOSE_NODES_FAILED}" -eq "1" ]
# then 
#     echo "Failed to choose requested nodes!\nTry ${try}\nTrying again in 1 min.\n"
#     sleep 60
#     continue 
# fi
# export CPUS_PER_TASK=24
# export PROCS_PER_NODE=2
# sbatch --nodes=6 --nodelist=${NODELIST} --ntasks-per-node=${PROCS_PER_NODE} --cpus-per-task=${CPUS_PER_TASK} --job-name=2PPN_topo_mxm \
# --output=${OUT_DIR}/slurmOutput2PPN.txt \
# --export=${MY_EXPORTS} \
# ${CUR_DIR}/run_experiments.sh
# break
# done

unset NODELIST