#/bin/bash

# load modules like Intel compiler, Intel MPI

export CUR_DATE_STR="$(date +"%Y%m%d_%H%M%S")"
CUR_DIR=$(pwd)
DIR_CH=${DIR_CH:-../../chameleon-lib/src}
DIR_MXM_EXAMPLE=${DIR_MXM_EXAMPLE:-../../chameleon-apps/applications/matrix_example}

#echo ${DIR_CH}

# define result dirs
export DIR_CH_REP4_BUILD=$(pwd)/chameleon_rep4_build
export DIR_CH_REP4_INSTALL=$(pwd)/chameleon_rep4_install

export DIR_CH_REP3_BUILD=$(pwd)/chameleon_rep3_build
export DIR_CH_REP3_INSTALL=$(pwd)/chameleon_rep3_install

export DIR_CH_REP2_BUILD=$(pwd)/chameleon_rep2_build
export DIR_CH_REP2_INSTALL=$(pwd)/chameleon_rep2_install

export DIR_CH_REP0_BUILD=$(pwd)/chameleon_rep0_build
export DIR_CH_REP0_INSTALL=$(pwd)/chameleon_rep0_install

if [ ${BUILD} ]
then
# Build regular version (chunk)
rm -rf ${DIR_CH_REP4_INSTALL}  && mkdir -p ${DIR_CH_REP4_INSTALL}/include && mkdir -p ${DIR_CH_REP4_INSTALL}/lib && cd ${DIR_CH}
INSTALL_DIR=${DIR_CH_REP4_INSTALL} CUSTOM_COMPILE_FLAGS="-DCHAM_STATS_RECORD -DCHAM_STATS_PRINT -DCHAM_REPLICATION_MODE=4" make release
cd ${CUR_DIR}

rm -rf ${DIR_CH_REP3_INSTALL}  && mkdir -p ${DIR_CH_REP3_INSTALL}/include && mkdir -p ${DIR_CH_REP3_INSTALL}/lib && cd ${DIR_CH}
INSTALL_DIR=${DIR_CH_REP3_INSTALL} CUSTOM_COMPILE_FLAGS="-DCHAM_STATS_RECORD -DCHAM_STATS_PRINT -DCHAM_REPLICATION_MODE=3" make release
cd ${CUR_DIR}

rm -rf ${DIR_CH_REP2_INSTALL}  && mkdir -p ${DIR_CH_REP2_INSTALL}/include && mkdir -p ${DIR_CH_REP2_INSTALL}/lib && cd ${DIR_CH}
INSTALL_DIR=${DIR_CH_REP2_INSTALL} CUSTOM_COMPILE_FLAGS="-DCHAM_STATS_RECORD -DCHAM_STATS_PRINT -DCHAM_REPLICATION_MODE=2" make release
cd ${CUR_DIR}

rm -rf ${DIR_CH_REP0_INSTALL}  && mkdir -p ${DIR_CH_REP0_INSTALL}/include && mkdir -p ${DIR_CH_REP0_INSTALL}/lib && cd ${DIR_CH}
INSTALL_DIR=${DIR_CH_REP0_INSTALL} CUSTOM_COMPILE_FLAGS="-DCHAM_STATS_RECORD -DCHAM_STATS_PRINT -DCHAM_REPLICATION_MODE=0" make release
cd ${CUR_DIR}

fi

# set env vars to use lib
export LD_LIBRARY_PATH="${DIR_CH_REP4_INSTALL}/lib:${LD_LIBRARY_PATH}"
export LIBRARY_PATH="${DIR_CH_REP4_INSTALL}/lib:${LIBRARY_PATH}"
export INCLUDE="${DIR_CH_REP4_INSTALL}/include:${INCLUDE}"
export CPATH="${DIR_CH_REP4_INSTALL}/include:${CPATH}"

# build matrix example
make clean -C ${DIR_MXM_EXAMPLE}
ITERATIVE_VERSION=1 NUM_ITERATIONS=100 make -C ${DIR_MXM_EXAMPLE}

# 2 node job - distributed memory
#export IS_DISTRIBUTED=1
#export IS_SEPARATE=0
#export N_PROCS=2

# set env vars to use lib
export LD_LIBRARY_PATH="${DIR_CH_REP4_INSTALL}/lib:${LD_LIBRARY_PATH}"
export LIBRARY_PATH="${DIR_CH_REP4_INSTALL}/lib:${LIBRARY_PATH}"
export INCLUDE="${DIR_CH_REP4_INSTALL}/include:${INCLUDE}"
export CPATH="${DIR_CH_REP4_INSTALL}/include:${CPATH}"

# build matrix example
make clean -C ${DIR_MXM_EXAMPLE}
ITERATIVE_VERSION=1 NUM_ITERATIONS=100 make -C ${DIR_MXM_EXAMPLE}

# 2 node job - distributed memory

export REP_MODE=0

sbatch --nodes=2 --ntasks-per-node=1 --cpus-per-task=48 --job-name=mxm_2n_rep --error=mxm_2n_rep.%J.err --output=mxm_2n_rep.%J.txt --export=REP_MODE,DIR_CH_REP0_INSTALL,DIR_CH_REP2_INSTALL,DIR_CH_REP3_INSTALL,DIR_CH_REP4_INSTALL,CUR_DATE_STR,N_PROCS run_experiments.sh
