#!/usr/local_rwth/bin/zsh

export CUR_DATE_STR=${CUR_DATE_STR:-"$(date +"%Y%m%d_%H%M%S")"}
export OUT_DIR="/home/ka387454/repos/chameleon-scripts/affinity_tests_mxm/outputs/output_"${CUR_DATE_STR}
#export OUT_DIR="/home/ka387454/repos/chameleon-scripts/affinity_tests_mxm/outputs/pageN"
mkdir ${OUT_DIR}


export_vars="OUT_DIR,CUR_DATE_STR,MXM_PARAMS"

#########################################################
#           Compile Matrix Example Versions             #
#########################################################
# export CHAMELEON_VERSION="chameleon/intel"

# cd /home/ka387454/repos/chameleon-apps/applications/matrix_example
# module use -a /home/ka387454/.modules
# module load $CHAMELEON_VERSION

# export COMPILE_CHAMELEON=1
# export COMPILE_TASKING=0
# export PROG="mxm_chameleon"
# make

# export COMPILE_CHAMELEON=0
# export COMPILE_TASKING=1
# export PROG="mxm_tasking"
# make

# cd -

#########################################################
#                       Tests                           #
#########################################################

# export MXM_PARAMS="600 1200"
# sbatch --nodes=1 --ntasks-per-node=1 --cpus-per-task=48 --job-name=mxm_affinity_testing \
# --output=${OUT_DIR}/slurmOutput.txt \
# --export=${export_vars} \
# run_experiments.sh

export MXM_PARAMS="600 1200 1200"
sbatch --nodes=2 --ntasks-per-node=1 --cpus-per-task=48 --job-name=mxm_affinity_testing \
--output=${OUT_DIR}/slurmOutput.txt \
--export=${export_vars} \
run_experiments.sh

# export MXM_PARAMS="600 1200 1200 1200 1200"
# sbatch --nodes=4 --ntasks-per-node=1 --cpus-per-task=48 --job-name=mxm_affinity_testing \
# --output=${OUT_DIR}/slurmOutput.txt \
# --export=${export_vars} \
# run_experiments.sh