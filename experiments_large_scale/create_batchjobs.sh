#!/usr/local_rwth/bin/zsh

# load modules like Intel compiler, Intel MPI
source env_ch_intel.sh
module unload chameleon-lib

export CUR_DATE_STR="$(date +"%Y%m%d_%H%M%S")"
CUR_DIR=$(pwd)
DIR_CH=${DIR_CH:-../../chameleon}
DIR_MXM_EXAMPLE=${DIR_MXM_EXAMPLE:-../../chameleon-apps/applications/matrix_example}
DIR_SAMOA=${DIR_SAMOA:-../../samoa-chameleon}
SAMOA_BUILD_PARAMS="target=release scenario=swe swe_patch_order=7 flux_solver=aug_riemann assertions=on compiler=intel"

# define result dirs
export DIR_CH_BUILD=$(pwd)/chameleon_build
export DIR_CH_INSTALL=$(pwd)/chameleon_install

rm -rf ${DIR_CH_BUILD} && mkdir -p ${DIR_CH_BUILD} && cd ${DIR_CH_BUILD}
cmake -DCMAKE_INSTALL_PREFIX=${DIR_CH_INSTALL} -DCMAKE_BUILD_TYPE=Release ${CUR_DIR}/${DIR_CH}
make -j8
make install

cd ${CUR_DIR}

# set env vars to use lib
export LD_LIBRARY_PATH="${DIR_CH_INSTALL}/lib:${LD_LIBRARY_PATH}"
export LIBRARY_PATH="${DIR_CH_INSTALL}/lib:${LIBRARY_PATH}"
export INCLUDE="${DIR_CH_INSTALL}/include:${INCLUDE}"
export CPATH="${DIR_CH_INSTALL}/include:${CPATH}"

# build matrix example
PROG=mxm_chameleon make clean -C ${DIR_MXM_EXAMPLE}
PROG=mxm_tasking make clean -C ${DIR_MXM_EXAMPLE}
PROG=mxm_chameleon COMPILE_TASKING=0 COMPILE_CHAMELEON=1 ITERATIVE_VERSION=0 make -C ${DIR_MXM_EXAMPLE}
PROG=mxm_tasking COMPILE_TASKING=1 COMPILE_CHAMELEON=0 ITERATIVE_VERSION=0 make -C ${DIR_MXM_EXAMPLE}

# build samoa
cd ${DIR_SAMOA}
rm -rf ${DIR_SAMOA}/bin/*
scons asagi=on ${SAMOA_BUILD_PARAMS} asagi_dir=/work/jk869269/repos/chameleon/ASAGI_install chameleon=2 -j8
scons asagi=on ${SAMOA_BUILD_PARAMS} asagi_dir=/work/jk869269/repos/chameleon/ASAGI_install chameleon=1 -j8

export N_NODES=4
export N_REPETITIONS=3

# ==================== Experiment 1: MxM Example - Check for manufacturing variations (power capping) ====================
export IS_CHAMELEON=1
export MXM_PROG_NAME=mxm_chameleon
# sbatch --nodes=${N_NODES} --job-name=experiment1_mxm_${N_NODES}nodes_cham --output=sbatch_experiment1_mxm_${N_NODES}nodes_cham.%J.txt --export=DIR_CH_INSTALL,CUR_DATE_STR,N_NODES,IS_CHAMELEON,N_REPETITIONS,MXM_PROG_NAME experiment1.sh

export IS_CHAMELEON=0
export MXM_PROG_NAME=mxm_tasking
# sbatch --nodes=${N_NODES} --job-name=experiment1_mxm_${N_NODES}nodes_task --output=sbatch_experiment1_mxm_${N_NODES}nodes_task.%J.txt --export=DIR_CH_INSTALL,CUR_DATE_STR,N_NODES,IS_CHAMELEON,N_REPETITIONS,MXM_PROG_NAME experiment1.sh

# ==================== Experiment 2: MxM Example - Frequency Manipulation (constant) ====================
export IS_CHAMELEON=1
export MXM_PROG_NAME=mxm_chameleon
#sbatch --nodes=${N_NODES} --job-name=experiment2_mxm_${N_NODES}nodes_cham --output=sbatch_experiment2_mxm_${N_NODES}nodes_cham.%J.txt --export=DIR_CH_INSTALL,CUR_DATE_STR,N_NODES,IS_CHAMELEON,N_REPETITIONS,MXM_PROG_NAME experiment2.sh

export IS_CHAMELEON=0
export MXM_PROG_NAME=mxm_tasking
# sbatch --nodes=${N_NODES} --job-name=experiment2_mxm_${N_NODES}nodes_task --output=sbatch_experiment2_mxm_${N_NODES}nodes_task.%J.txt --export=DIR_CH_INSTALL,CUR_DATE_STR,N_NODES,IS_CHAMELEON,N_REPETITIONS,MXM_PROG_NAME experiment2.sh

# ==================== Experiment 4: MxM Example - Unbalanced ====================
export IS_CHAMELEON=1
export MXM_PROG_NAME=mxm_chameleon
sbatch --nodes=${N_NODES} --job-name=experiment4_mxm_${N_NODES}nodes_cham --output=sbatch_experiment4_mxm_${N_NODES}nodes_cham.%J.txt --export=DIR_CH_INSTALL,CUR_DATE_STR,N_NODES,IS_CHAMELEON,N_REPETITIONS,MXM_PROG_NAME experiment4.sh

export IS_CHAMELEON=0
export MXM_PROG_NAME=mxm_tasking
sbatch --nodes=${N_NODES} --job-name=experiment4_mxm_${N_NODES}nodes_task --output=sbatch_experiment4_mxm_${N_NODES}nodes_task.%J.txt --export=DIR_CH_INSTALL,CUR_DATE_STR,N_NODES,IS_CHAMELEON,N_REPETITIONS,MXM_PROG_NAME experiment4.sh
