#!/usr/local_rwth/bin/zsh

# ========================================
# Global Settings
# ========================================
CUR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )" # get path of current script

export RUN_LIKWID=1
# IMBALANCED=(0 1)
export CUR_DATE_STR=${CUR_DATE_STR:-"$(date +"%Y%m%d_%H%M%S")"}
export OUT_DIR="${CUR_DIR}/outputs/output_"${CUR_DATE_STR}
mkdir -p ${OUT_DIR}

export_vars="OUT_DIR,CUR_DATE_STR,MXM_PARAMS,CPUS_PER_TASK,MXM_SIZE,MXM_DISTRIBUTION,PROCS_PER_NODE,SOME_INDEX,NODES,RUN_LIKWID"

#########################################################
#           Compile Chameleon Versions                  #
#########################################################
cd ${CUR_DIR}/../../chameleon/src
export INSTALL_DIR=~/install/chameleon/intel_affinity_debug
# make aff_debug
make aff_no_commthread

export INSTALL_DIR=~/install/chameleon/intel_no_affinity
CUSTOM_COMPILE_FLAGS="-DUSE_TASK_AFFINITY=0" make

export INSTALL_DIR=~/install/chameleon/intel
make
cd -

#########################################################
#           Compile Matrix Example Versions             #
#########################################################
module load likwid

export CHAMELEON_VERSION="chameleon/intel"

cd ${CUR_DIR}/../../chameleon-apps/applications/matrix_example
source ~/.zshrc
module load $CHAMELEON_VERSION

export COMPILE_CHAMELEON=1
export COMPILE_TASKING=0
export PROG="mxm_chameleon"
make likwid

export COMPILE_CHAMELEON=0
export COMPILE_TASKING=1
export PROG="mxm_tasking"
make likwid

cd ${CUR_DIR}

#########################################################
#                       Tests                           #
#########################################################

###################### 1 Node ###########################
export MXM_SIZE=600
export MXM_DISTRIBUTION="1200"
export CPUS_PER_TASK=48
sbatch --nodes=1 --ntasks-per-node=1 --cpus-per-task=${CPUS_PER_TASK} --job-name=mxm_affinity_testing \
    --output=${OUT_DIR}/slurmOutput.txt \
    --export=${export_vars} \
    run_experiments.sh

# for imb in "${IMBALANCED[@]}"
# do
#     export IS_IMBALANCED=${imb}

#     # 2 rank job - shared memory
#     export N_PROCS=2
#     sbatch --nodes=1 --ntasks-per-node=2 --cpus-per-task=24 --job-name=mxm_2procs_sm --output=mxm_2procs_sm.%J.txt --export=IS_IMBALANCED,RUN_LIKWID,CUR_DATE_STR,N_PROCS run_experiments.sh

#     # 4 rank job - shared memory
#     export N_PROCS=4
#     sbatch --nodes=1 --ntasks-per-node=4 --cpus-per-task=12 --job-name=mxm_4procs_sm --output=mxm_4procs_sm.%J.txt --export=IS_IMBALANCED,RUN_LIKWID,CUR_DATE_STR,N_PROCS run_experiments.sh

#     # 4 rank job - distributed memory
#     export N_PROCS=4
#     sbatch --nodes=2 --ntasks-per-node=2 --cpus-per-task=24 --job-name=mxm_4procs_dm --output=mxm_4procs_dm.%J.txt --export=IS_IMBALANCED,RUN_LIKWID,CUR_DATE_STR,N_PROCS run_experiments.sh
# done
