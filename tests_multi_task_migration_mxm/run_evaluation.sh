#!/usr/local_rwth/bin/zsh

# =============== Load desired modules
source env_ch_intel.sh

# =============== Settings & environment variables
DIR_CH_SRC=${DIR_CH_SRC:-../../chameleon-lib/src/}
DIR_MXM_EXAMPLE=${DIR_MXM_EXAMPLE:-../../chameleon-lib/examples/matrix_example/}

# TASK_GRANULARITY=(50,100,150,200,250)
# N_THREADS=(2,4,8)
TASK_GRANULARITY=(250)
N_THREADS=(4)
N_TASKS=1000
N_REPETITIONS=1
IS_DISTRIBUTED_JOB=1

# Run settings
# OMP_PLACES=cores
# OMP_PROC_BIND=close
# KMP_AFFINITY=verbose
# I_MPI_DEBUG=5
# I_MPI_PIN=1
# I_MPI_PIN_DOMAIN=auto
# I_MPI_FABRICS="shm:tmi"

export MIN_REL_LOAD_IMBALANCE_BEFORE_MIGRATION=0.1
export MAX_TASKS_PER_RANK_TO_MIGRATE_AT_ONCE=50

# =============== Build library
# build library with multi task offloading
make clean -C ${DIR_CH_SRC}
TARGET=claix_intel INSTALL_DIR=~/install/chameleon-lib/intel_1.0 make -C ${DIR_CH_SRC}

# build matrx example
# make clean -C ${DIR_MXM_EXAMPLE}
# ITERATIVE_VERSION=0 make -C ${DIR_MXM_EXAMPLE}

# source ../../chameleon-lib/flags_claix_intel.def
# echo "${RUN_SETTINGS}"

# for g in "${TASK_GRANULARITY[@]}"
# do
#     for t in "${N_THREADS[@]}"
#     do
#         export MIN_LOCAL_TASKS_IN_QUEUE_BEFORE_MIGRATION=$t
#         echo "${RUN_SETTINGS} mpiexec.hydra -np 2 ${MPI_EXPORT_VARS} ${DIR_MXM_EXAMPLE}/main $g ${N_TASKS} 0"
#     done
# done

