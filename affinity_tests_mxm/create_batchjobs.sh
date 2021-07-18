#!/usr/local_rwth/bin/zsh

export CUR_DATE_STR=${CUR_DATE_STR:-"$(date +"%Y%m%d_%H%M%S")"}
export CUR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )" # get path of current script
export OUT_DIR="${CUR_DIR}/outputs/output_"${CUR_DATE_STR}
# export OUT_DIR="${CUR_DIR}/outputs/stats_mapMode_CheckPhy_NoNuma_1Node_PageChangeCheck"
mkdir -p ${OUT_DIR}


MY_EXPORTS="OUT_DIR,CUR_DATE_STR,MXM_PARAMS,CPUS_PER_TASK,MXM_SIZE,MXM_DISTRIBUTION,PROCS_PER_NODE,SOME_INDEX,NODES,CUR_DIR"

#########################################################
#           Compile Chameleon Versions                  #
#########################################################
# cd ${CUR_DIR}/../../chameleon/src
# export INSTALL_DIR=~/install/chameleon/intel_affinity_debug
# make aff_debug

# export INSTALL_DIR=~/install/chameleon/intel_no_affinity
# CUSTOM_COMPILE_FLAGS="-DUSE_TASK_AFFINITY=0" make

# export INSTALL_DIR=~/install/chameleon/intel
# make
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
# export MXM_SIZE=600
# export MXM_DISTRIBUTION="1200"
# export CPUS_PER_TASK=48
# sbatch --nodes=1 --ntasks-per-node=1 --cpus-per-task=${CPUS_PER_TASK} --job-name=mxm_affinity_testing \
# --output=${OUT_DIR}/slurmOutput.txt \
# --export=${MY_EXPORTS} \
# run_experiments.sh

###################### 2 Nodes ##########################
export MXM_SIZE=600
export MXM_DISTRIBUTION="1200 1200"
export CPUS_PER_TASK=48
sbatch --nodes=2 --ntasks-per-node=1 --cpus-per-task=${CPUS_PER_TASK} --job-name=mxm_affinity_testing \
--output=${OUT_DIR}/slurmOutput.txt \
--export=${MY_EXPORTS} \
run_experiments.sh


#########################################################
#                Vary Procs per Node                    #
#########################################################
# export MXM_SIZE=600
# distributions=(         # in zsh iterator starts with 1!
#     "1200 1200"                         # 1
#     "600 600 600 600"                   # 2
#     "-"                                 # 3
#     "300 300 300 300 300 300 300 300"   # 4
# )
# for PPN in 1 2 4
# do
#     export MXM_DISTRIBUTION="${distributions[${PPN}]}"
#     export PROCS_PER_NODE="${PPN}"
#     export CPUS_PER_TASK="$((48/${PPN}))"
#     sbatch --nodes=2 --ntasks-per-node=${PPN} --cpus-per-task=${CPUS_PER_TASK} --job-name=mxm_affinity_testing \
#     --output=${OUT_DIR}/slurmOutput_${PPN}.txt \
#     --export=${MY_EXPORTS} \
#     run_experiments.sh
# done

#########################################################
#                Vary Number of Slurm Nodes             #
#########################################################
# export MXM_SIZE=600
# tasks=1200
# export PROCS_PER_NODE=1
# export CPUS_PER_TASK=48
# export SOME_INDEX=0
# for NODES in 1 2 4 8 16 32
# do
#     export NODES
#     export SOME_INDEX=$(($SOME_INDEX+1))    # for plotting
#     # echo ${SOME_INDEX}
#     MXM_DISTRIBUTION=""
#     if [ "${NODES}" -gt "1" ]
#     then
#         for x in {1..$((${NODES}-1))}
#         do
#             MXM_DISTRIBUTION=${MXM_DISTRIBUTION}${tasks}" "
#         done
#     fi
#     MXM_DISTRIBUTION=${MXM_DISTRIBUTION}${tasks}
#     export MXM_DISTRIBUTION
#     # echo ${MXM_DISTRIBUTION}
#     sbatch --nodes=${NODES} --ntasks-per-node=${PROCS_PER_NODE} --cpus-per-task=${CPUS_PER_TASK} --job-name=mxm_affinity_testing \
#     --output=${OUT_DIR}/slurmOutput_${NODES}.txt \
#     --export=${MY_EXPORTS} \
#     run_experiments.sh
# done