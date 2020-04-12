#!/usr/local_rwth/bin/zsh

# load modules like Intel compiler, Intel MPI
source env_ch_intel.sh
module unload chameleon-lib

export CUR_DATE_STR="$(date +"%Y%m%d_%H%M%S")"
CUR_DIR=$(pwd)
DIR_CH=${DIR_CH:-../../chameleon}
DIR_MXM_EXAMPLE=${DIR_MXM_EXAMPLE:-../../chameleon-apps/applications/matrix_example}

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

export N_NODES=16
export N_REPETITIONS=3

# ==================== Experiment 1: MxM Example - Check for manufacturing variations (power capping) ====================
export IS_CHAMELEON=1
export MXM_PROG_NAME=mxm_chameleon
sbatch --nodes=${N_NODES} --job-name=experiment1_mxm_${N_NODES}_nodes --output=experiment1_mxm_${N_NODES}_nodes.%J.txt --export=DIR_CH_INSTALL,CUR_DATE_STR,N_NODES run_experiments.sh
