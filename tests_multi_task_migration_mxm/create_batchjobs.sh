#!/usr/local_rwth/bin/zsh

source env_ch_intel.sh

export CUR_DATE_STR="$(date +"%Y%m%d_%H%M%S")"
DIR_CH_SRC=${DIR_CH_SRC:-../../chameleon-lib/src}
DIR_MXM_EXAMPLE=${DIR_MXM_EXAMPLE:-../../chameleon-lib/examples/matrix_example}

# Build regular chunk version 
make clean -C ${DIR_CH_SRC}
TARGET=claix_intel INSTALL_DIR=~/install/chameleon-lib/intel_1.0 make -C ${DIR_CH_SRC}
# Build version with separate sends
make clean -C ${DIR_CH_SRC}
TARGET=claix_intel INSTALL_DIR=~/install/chameleon-lib/intel_1.0_separate CUSTOM_COMPILE_FLAGS='-DOFFLOAD_SEND_TASKS_SEPARATELY=1' make -C ${DIR_CH_SRC}
# build matrix example
make clean -C ${DIR_MXM_EXAMPLE}
ITERATIVE_VERSION=0 make -C ${DIR_MXM_EXAMPLE}

# 2 node job - shared memory
export IS_DISTRIBUTED=0
export IS_SEPARATE=0
export N_PROCS=2
sbatch --nodes=1 --ntasks-per-node=2 --cpus-per-task=12 --job-name=mxm_multi_task_migration_2n_sm --output=mxm_multi_task_migration_2n_sm.%J.txt --export=IS_DISTRIBUTED,IS_SEPARATE,CUR_DATE_STR,N_PROCS run_experiments.sh
export IS_SEPARATE=1
sbatch --nodes=1 --ntasks-per-node=2 --cpus-per-task=12 --job-name=mxm_multi_task_migration_2n_sm_sep --output=mxm_multi_task_migration_2n_sm_sep.%J.txt --export=IS_DISTRIBUTED,IS_SEPARATE,CUR_DATE_STR,N_PROCS run_experiments.sh

# 2 node job - distributed memory
export IS_DISTRIBUTED=1
export IS_SEPARATE=0
export N_PROCS=2
sbatch --nodes=2 --ntasks-per-node=1 --cpus-per-task=24 --job-name=mxm_multi_task_migration_2n_dm --output=mxm_multi_task_migration_2n_dm.%J.txt --export=IS_DISTRIBUTED,IS_SEPARATE,CUR_DATE_STR,N_PROCS run_experiments.sh
export IS_SEPARATE=1
sbatch --nodes=2 --ntasks-per-node=1 --cpus-per-task=24 --job-name=mxm_multi_task_migration_2n_dm_sep --output=mxm_multi_task_migration_2n_dm_sep.%J.txt --export=IS_DISTRIBUTED,IS_SEPARATE,CUR_DATE_STR,N_PROCS run_experiments.sh

# 4 node job - shared memory
export IS_DISTRIBUTED=0
export IS_SEPARATE=0
export N_PROCS=4
sbatch --nodes=1 --ntasks-per-node=4 --cpus-per-task=6 --job-name=mxm_multi_task_migration_4n_sm --output=mxm_multi_task_migration_4n_sm.%J.txt --export=IS_DISTRIBUTED,IS_SEPARATE,CUR_DATE_STR,N_PROCS run_experiments.sh
export IS_SEPARATE=1
sbatch --nodes=1 --ntasks-per-node=4 --cpus-per-task=6 --job-name=mxm_multi_task_migration_4n_sm_sep --output=mxm_multi_task_migration_4n_sm_sep.%J.txt --export=IS_DISTRIBUTED,IS_SEPARATE,CUR_DATE_STR,N_PROCS run_experiments.sh

# 4 node job - distributed memory
export IS_DISTRIBUTED=1
export IS_SEPARATE=0
export N_PROCS=4
sbatch --nodes=4 --ntasks-per-node=1 --cpus-per-task=24 --job-name=mxm_multi_task_migration_4n_dm --output=mxm_multi_task_migration_4n_dm.%J.txt --export=IS_DISTRIBUTED,IS_SEPARATE,CUR_DATE_STR,N_PROCS run_experiments.sh
export IS_SEPARATE=1
sbatch --nodes=4 --ntasks-per-node=1 --cpus-per-task=24 --job-name=mxm_multi_task_migration_4n_dm_sep --output=mxm_multi_task_migration_4n_dm_sep.%J.txt --export=IS_DISTRIBUTED,IS_SEPARATE,CUR_DATE_STR,N_PROCS run_experiments.sh

# 8 node job - distributed memory
export IS_DISTRIBUTED=1
export IS_SEPARATE=0
export N_PROCS=8
sbatch --nodes=8 --ntasks-per-node=1 --cpus-per-task=24 --job-name=mxm_multi_task_migration_8n_dm --output=mxm_multi_task_migration_8n_dm.%J.txt --export=IS_DISTRIBUTED,IS_SEPARATE,CUR_DATE_STR,N_PROCS run_experiments.sh
export IS_SEPARATE=1
sbatch --nodes=8 --ntasks-per-node=1 --cpus-per-task=24 --job-name=mxm_multi_task_migration_8n_dm_sep --output=mxm_multi_task_migration_8n_dm_sep.%J.txt --export=IS_DISTRIBUTED,IS_SEPARATE,CUR_DATE_STR,N_PROCS run_experiments.sh

