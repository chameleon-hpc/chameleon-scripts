#!/usr/local_rwth/bin/zsh

export CUR_DATE_STR=${CUR_DATE_STR:-"$(date +"%Y%m%d_%H%M%S")"}
export OUT_DIR="/home/ka387454/repos/chameleon-scripts/affinity_tests_mxm/outputs/output_"${CUR_DATE_STR}
#export OUT_DIR="/home/ka387454/repos/chameleon-scripts/affinity_tests_mxm/outputs/mapMode_CheckPhy_NumaBal"
mkdir ${OUT_DIR}


export_vars="OUT_DIR,CUR_DATE_STR,MXM_PARAMS,CPUS_PER_TASK"

#########################################################
#           Compile Chameleon Versions                  #
#########################################################
cd /home/ka387454/repos/chameleon/src
export INSTALL_DIR=~/install/chameleon/intel_affinity_debug
make aff_debug

export INSTALL_DIR=~/install/chameleon/intel_no_affinity
CUSTOM_COMPILE_FLAGS="-DUSE_TASK_AFFINITY=0" make

export INSTALL_DIR=~/install/chameleon/intel
make
cd -

#########################################################
#           Compile Matrix Example Versions             #
#########################################################
export CHAMELEON_VERSION="chameleon/intel"

cd /home/ka387454/repos/chameleon-apps/applications/matrix_example
module use -a /home/ka387454/.modules
module load $CHAMELEON_VERSION

export COMPILE_CHAMELEON=1
export COMPILE_TASKING=0
export PROG="mxm_chameleon"
make

export COMPILE_CHAMELEON=0
export COMPILE_TASKING=1
export PROG="mxm_tasking"
make

cd -

#########################################################
#                       Tests                           #
#########################################################

# export MXM_PARAMS="600 1200"
# sbatch --nodes=1 --ntasks-per-node=1 --cpus-per-task=48 --job-name=mxm_affinity_testing \
# --output=${OUT_DIR}/slurmOutput.txt \
# --export=${export_vars} \
# run_experiments.sh

export MXM_PARAMS="600 1200 1200"
export CPUS_PER_TASK=48
sbatch --nodes=2 --ntasks-per-node=1 --cpus-per-task=${CPUS_PER_TASK} --job-name=mxm_affinity_testing \
--output=${OUT_DIR}/slurmOutput.txt \
--export=${export_vars} \
run_experiments.sh

# export MXM_PARAMS="600 1200 1200 1200 1200"
# sbatch --nodes=4 --ntasks-per-node=1 --cpus-per-task=48 --job-name=mxm_affinity_testing \
# --output=${OUT_DIR}/slurmOutput.txt \
# --export=${export_vars} \
# run_experiments.sh

###         Sanity check, here should be no big diff between chameleon and no chameleon     ###
# adjust OMP_NUM_THREADS in run_experiments!
# export MXM_PARAMS="600 600 600 600 600"
# sbatch --nodes=2 --ntasks-per-node=2 --cpus-per-task=24 --job-name=mxm_affinity_testing \
# --output=${OUT_DIR}/slurmOutput.txt \
# --export=${export_vars} \
# run_experiments.sh