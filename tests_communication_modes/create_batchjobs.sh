#!/usr/local_rwth/bin/zsh

# load modules like Intel compiler, Intel MPI
source env_ch_intel.sh
module unload chameleon-lib

export CUR_DATE_STR="$(date +"%Y%m%d_%H%M%S")"
CUR_DIR=$(pwd)
DIR_CH=${DIR_CH:-../../../chameleon}
DIR_MXM_EXAMPLE=${DIR_MXM_EXAMPLE:-../../chameleon-apps/applications/matrix_example}

# define result dirs
export DIR_CH_MODE0_BUILD=$(pwd)/chameleon_mode0_build
export DIR_CH_MODE0_INSTALL=$(pwd)/chameleon_mode0_install
export DIR_CH_MODE1_BUILD=$(pwd)/chameleon_mode1_build
export DIR_CH_MODE1_INSTALL=$(pwd)/chameleon_mode1_install
export DIR_CH_MODE2_BUILD=$(pwd)/chameleon_mode2_build
export DIR_CH_MODE2_INSTALL=$(pwd)/chameleon_mode2_install
export DIR_CH_MODE3_BUILD=$(pwd)/chameleon_mode3_build
export DIR_CH_MODE3_INSTALL=$(pwd)/chameleon_mode3_install

# Build versions
for VAR in 0 1 2 3
do
    name_build="DIR_CH_MODE${VAR}_BUILD"
    name_install="DIR_CH_MODE${VAR}_INSTALL"
    eval cur_build=\$${name_build}
    eval cur_install=\$${name_install}

    rm -rf ${cur_build} && mkdir ${cur_build} && cd ${cur_build}
    cmake -DCMAKE_INSTALL_PREFIX=${cur_install} -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS="-DCOMMUNICATION_MODE=${VAR}" -DCMAKE_C_FLAGS="-DCOMMUNICATION_MODE=${VAR}" ${DIR_CH}
    make -j8
    make install
done
cd ${CUR_DIR}

# set env vars to use lib
export LD_LIBRARY_PATH="${DIR_CH_MODE0_INSTALL}/lib:${LD_LIBRARY_PATH}"
export LIBRARY_PATH="${DIR_CH_MODE0_INSTALL}/lib:${LIBRARY_PATH}"
export INCLUDE="${DIR_CH_MODE0_INSTALL}/include:${INCLUDE}"
export CPATH="${DIR_CH_MODE0_INSTALL}/include:${CPATH}"

# build matrix example
make clean -C ${DIR_MXM_EXAMPLE}
ITERATIVE_VERSION=0 make -C ${DIR_MXM_EXAMPLE}

: << COMMENT
# 2 node job - shared memory
export IS_DISTRIBUTED=0
export N_PROCS=2
sbatch --nodes=1 --ntasks-per-node=2 --cpus-per-task=12 --job-name=mxm_communication_modes_2n_sm --output=mxm_communication_modes_2n_sm.%J.txt --export=DIR_CH_MODE0_INSTALL,DIR_CH_MODE1_INSTALL,DIR_CH_MODE2_INSTALL,DIR_CH_MODE3_INSTALL,IS_DISTRIBUTED,CUR_DATE_STR,N_PROCS run_experiments.sh
COMMENT

# 2 node job - distributed memory
export IS_DISTRIBUTED=1
export N_PROCS=2
sbatch --nodes=2 --ntasks-per-node=1 --cpus-per-task=24 --job-name=mxm_communication_modes_2n_dm --output=mxm_communication_modes_2n_dm.%J.txt --export=DIR_CH_MODE0_INSTALL,DIR_CH_MODE1_INSTALL,DIR_CH_MODE2_INSTALL,DIR_CH_MODE3_INSTALL,IS_DISTRIBUTED,CUR_DATE_STR,N_PROCS run_experiments.sh

: << COMMENT
# 4 node job - shared memory
export IS_DISTRIBUTED=0
export N_PROCS=4
sbatch --nodes=1 --ntasks-per-node=4 --cpus-per-task=6 --job-name=mxm_communication_modes_4n_sm --output=mxm_communication_modes_4n_sm.%J.txt --export=DIR_CH_MODE0_INSTALL,DIR_CH_MODE1_INSTALL,DIR_CH_MODE2_INSTALL,DIR_CH_MODE3_INSTALL,IS_DISTRIBUTED,CUR_DATE_STR,N_PROCS run_experiments.sh
COMMENT

# 4 node job - distributed memory
: << COMMENT
export IS_DISTRIBUTED=1
export N_PROCS=4
sbatch --nodes=4 --ntasks-per-node=1 --cpus-per-task=24 --job-name=mxm_communication_modes_4n_dm --output=mxm_communication_modes_4n_dm.%J.txt --export=DIR_CH_MODE0_INSTALL,DIR_CH_MODE1_INSTALL,DIR_CH_MODE2_INSTALL,DIR_CH_MODE3_INSTALL,IS_DISTRIBUTED,CUR_DATE_STR,N_PROCS run_experiments.sh
COMMENT

: << COMMENT
# 8 node job - distributed memory
export IS_DISTRIBUTED=1
export N_PROCS=8
sbatch --nodes=8 --ntasks-per-node=1 --cpus-per-task=24 --job-name=mxm_communication_modes_8n_dm --output=mxm_communication_modes_8n_dm.%J.txt --export=DIR_CH_MODE0_INSTALL,DIR_CH_MODE1_INSTALL,DIR_CH_MODE2_INSTALL,DIR_CH_MODE3_INSTALL,IS_DISTRIBUTED,CUR_DATE_STR,N_PROCS run_experiments.sh
COMMENT
