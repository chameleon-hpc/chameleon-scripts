#!/usr/local_rwth/bin/zsh

# load modules like Intel compiler, Intel MPI
source env_ch_intel.sh
module unload chameleon-lib

export CUR_DATE_STR="$(date +"%Y%m%d_%H%M%S")"
CUR_DIR=$(pwd)
DIR_CH=${DIR_CH:-../../../chameleon}
DIR_MXM_EXAMPLE=${DIR_MXM_EXAMPLE:-../../chameleon-apps/applications/matrix_example}

# define result dirs
export DIR_CH_REGULAR_BUILD=$(pwd)/chameleon_regular_build
export DIR_CH_REGULAR_INSTALL=$(pwd)/chameleon_regular_install
export DIR_CH_SEPARATE_BUILD=$(pwd)/chameleon_separate_build
export DIR_CH_SEPARATE_INSTALL=$(pwd)/chameleon_separate_install

# Build regular version (chunk)
rm -rf ${DIR_CH_REGULAR_BUILD} && mkdir ${DIR_CH_REGULAR_BUILD} && cd ${DIR_CH_REGULAR_BUILD}
cmake -DCMAKE_INSTALL_PREFIX=${DIR_CH_REGULAR_INSTALL} -DCMAKE_BUILD_TYPE=Release ${DIR_CH}
make -j8
make install
cd ${CUR_DIR}

# Build version with sepearte offloads
rm -rf ${DIR_CH_SEPARATE_BUILD} && mkdir ${DIR_CH_SEPARATE_BUILD} && cd ${DIR_CH_SEPARATE_BUILD}
cmake -DCMAKE_INSTALL_PREFIX=${DIR_CH_SEPARATE_INSTALL} -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS='-DOFFLOAD_SEND_TASKS_SEPARATELY=1' -DCMAKE_C_FLAGS='-DOFFLOAD_SEND_TASKS_SEPARATELY=1' ${DIR_CH}
make -j8
make install
cd ${CUR_DIR}

# set env vars to use lib
export LD_LIBRARY_PATH="${DIR_CH_REGULAR_INSTALL}/lib:${LD_LIBRARY_PATH}"
export LIBRARY_PATH="${DIR_CH_REGULAR_INSTALL}/lib:${LIBRARY_PATH}"
export INCLUDE="${DIR_CH_REGULAR_INSTALL}/include:${INCLUDE}"
export CPATH="${DIR_CH_REGULAR_INSTALL}/include:${CPATH}"

# build matrix example
make clean -C ${DIR_MXM_EXAMPLE}
ITERATIVE_VERSION=0 make -C ${DIR_MXM_EXAMPLE}

: << COMMENT
# 2 node job - shared memory
export IS_DISTRIBUTED=0
export IS_SEPARATE=0
export N_PROCS=2
sbatch --nodes=1 --ntasks-per-node=2 --cpus-per-task=12 --job-name=mxm_multi_task_migration_2n_sm --output=mxm_multi_task_migration_2n_sm.%J.txt --export=DIR_CH_REGULAR_INSTALL,DIR_CH_SEPARATE_INSTALL,IS_DISTRIBUTED,IS_SEPARATE,CUR_DATE_STR,N_PROCS run_experiments.sh
export IS_SEPARATE=1
sbatch --nodes=1 --ntasks-per-node=2 --cpus-per-task=12 --job-name=mxm_multi_task_migration_2n_sm_sep --output=mxm_multi_task_migration_2n_sm_sep.%J.txt --export=DIR_CH_REGULAR_INSTALL,DIR_CH_SEPARATE_INSTALL,IS_DISTRIBUTED,IS_SEPARATE,CUR_DATE_STR,N_PROCS run_experiments.sh
COMMENT

# 2 node job - distributed memory
export IS_DISTRIBUTED=1
export IS_SEPARATE=0
export N_PROCS=2
sbatch --nodes=2 --ntasks-per-node=1 --cpus-per-task=24 --job-name=mxm_multi_task_migration_2n_dm --output=mxm_multi_task_migration_2n_dm.%J.txt --export=DIR_CH_REGULAR_INSTALL,DIR_CH_SEPARATE_INSTALL,IS_DISTRIBUTED,IS_SEPARATE,CUR_DATE_STR,N_PROCS run_experiments.sh
#export IS_SEPARATE=1
#sbatch --nodes=2 --ntasks-per-node=1 --cpus-per-task=24 --job-name=mxm_multi_task_migration_2n_dm_sep --output=mxm_multi_task_migration_2n_dm_sep.%J.txt --export=DIR_CH_REGULAR_INSTALL,DIR_CH_SEPARATE_INSTALL,IS_DISTRIBUTED,IS_SEPARATE,CUR_DATE_STR,N_PROCS run_experiments.sh

: << COMMENT
# 4 node job - shared memory
export IS_DISTRIBUTED=0
export IS_SEPARATE=0
export N_PROCS=4
sbatch --nodes=1 --ntasks-per-node=4 --cpus-per-task=6 --job-name=mxm_multi_task_migration_4n_sm --output=mxm_multi_task_migration_4n_sm.%J.txt --export=DIR_CH_REGULAR_INSTALL,DIR_CH_SEPARATE_INSTALL,IS_DISTRIBUTED,IS_SEPARATE,CUR_DATE_STR,N_PROCS run_experiments.sh
export IS_SEPARATE=1
sbatch --nodes=1 --ntasks-per-node=4 --cpus-per-task=6 --job-name=mxm_multi_task_migration_4n_sm_sep --output=mxm_multi_task_migration_4n_sm_sep.%J.txt --export=DIR_CH_REGULAR_INSTALL,DIR_CH_SEPARATE_INSTALL,IS_DISTRIBUTED,IS_SEPARATE,CUR_DATE_STR,N_PROCS run_experiments.sh
COMMENT

# 4 node job - distributed memory
export IS_DISTRIBUTED=1
export IS_SEPARATE=0
export N_PROCS=4
sbatch --nodes=4 --ntasks-per-node=1 --cpus-per-task=24 --job-name=mxm_multi_task_migration_4n_dm --output=mxm_multi_task_migration_4n_dm.%J.txt --export=DIR_CH_REGULAR_INSTALL,DIR_CH_SEPARATE_INSTALL,IS_DISTRIBUTED,IS_SEPARATE,CUR_DATE_STR,N_PROCS run_experiments.sh
#export IS_SEPARATE=1
#sbatch --nodes=4 --ntasks-per-node=1 --cpus-per-task=24 --job-name=mxm_multi_task_migration_4n_dm_sep --output=mxm_multi_task_migration_4n_dm_sep.%J.txt --export=DIR_CH_REGULAR_INSTALL,DIR_CH_SEPARATE_INSTALL,IS_DISTRIBUTED,IS_SEPARATE,CUR_DATE_STR,N_PROCS run_experiments.sh

: << COMMENT
# 8 node job - distributed memory
export IS_DISTRIBUTED=1
export IS_SEPARATE=0
export N_PROCS=8
sbatch --nodes=8 --ntasks-per-node=1 --cpus-per-task=24 --job-name=mxm_multi_task_migration_8n_dm --output=mxm_multi_task_migration_8n_dm.%J.txt --export=DIR_CH_REGULAR_INSTALL,DIR_CH_SEPARATE_INSTALL,IS_DISTRIBUTED,IS_SEPARATE,CUR_DATE_STR,N_PROCS run_experiments.sh
export IS_SEPARATE=1
sbatch --nodes=8 --ntasks-per-node=1 --cpus-per-task=24 --job-name=mxm_multi_task_migration_8n_dm_sep --output=mxm_multi_task_migration_8n_dm_sep.%J.txt --export=DIR_CH_REGULAR_INSTALL,DIR_CH_SEPARATE_INSTALL,IS_DISTRIBUTED,IS_SEPARATE,CUR_DATE_STR,N_PROCS run_experiments.sh
COMMENT
