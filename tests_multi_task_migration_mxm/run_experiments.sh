#!/usr/local_rwth/bin/zsh
#SBATCH --job-name=mxm_multi_task_migration
#SBATCH --output=output_mxm_multi_task_migration.%J.txt
#SBATCH --time=04:00:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=24
#SBATCH --exclusive
#SBATCH --account=jara0001
#SBATCH --partition=c16m

# =============== Load desired modules
source /home/jk869269/.zshrc
source env_ch_intel.sh

export CUR_DATE_STR="$(date +"%Y%m%d_%H%M%S")"

# # hack because currently vtune is not supported in batch usage
# module load c_vtune
# export CMD_VTUNE_PREFIX="amplxe-cl –collect hotspots –r ./${CUR_DATE_STR}_profiling_chameleon_${OMP_NUM_THREADS}t -trace-mpi -- "

# =============== Settings & environment variables
DIR_CH_SRC=${DIR_CH_SRC:-../../chameleon-lib/src}
DIR_MXM_EXAMPLE=${DIR_MXM_EXAMPLE:-../../chameleon-lib/examples/matrix_example}
DIR_RESULT="${CUR_DATE_STR}_results"

# create result directory
mkdir -p ${DIR_RESULT}

IS_DISTRIBUTED=1
N_PROCS=2
TASK_GRANULARITY=(50 100 150 200 250 300 350 400)
N_REPETITIONS=1
# TODO: maybe also permutate MAX_TASKS_PER_RANK_TO_MIGRATE_AT_ONCE

# default number of threads for distributed runs
N_THREADS=(1 2 4 6 8 10 12 14 16 18 20 22)

case ${N_PROCS} in
    2)
        echo "Running with 2 procs"
        MXM_PARAMS="1000 0"
        if [ "${IS_DISTRIBUTED}" = "0" ]; then
            N_THREADS=(1 2 3 4 5 6 7 8 9 10 11)
        fi
        ;;
    4)
        echo "Running with 4 procs"
        MXM_PARAMS="1000 667 333 0"
        if [ "${IS_DISTRIBUTED}" = "0" ]; then
            N_THREADS=(1 2 3 4 5)
        fi
        ;;
    8)
        echo "Running with 8 procs"
        MXM_PARAMS="1000 860 714 571 428 285 142 0"
        if [ "${IS_DISTRIBUTED}" = "0" ]; then
            echo "ERROR: Sorry script does not support shared memory job with 8 procs. Aborting here"
            exit 2
        fi
        ;;
    *)
        echo "ERROR: Sorry script does not support number of threads. Aborting here"
        exit 2
    esac

export MIN_REL_LOAD_IMBALANCE_BEFORE_MIGRATION=0.1
export MAX_TASKS_PER_RANK_TO_MIGRATE_AT_ONCE=30
export PERCENTAGE_DIFF_TASKS_TO_MIGRATE=0.4

# load flags
source ../../chameleon-lib/flags_claix_intel.def

if [ "${IS_DISTRIBUTED}" = "0" ]; then
    MPI_EXEC_CMD="${RUN_SETTINGS} mpiexec.hydra"
else
    MPI_EXEC_CMD="${RUN_SETTINGS} mpiexec"
fi

# =============== Execution Function
function run_experiments()
{
    exec_version=$1
    if [ "${IS_DISTRIBUTED}" = "0" ]; then
        exec_version="${exec_version}_sm"
    else
        exec_version="${exec_version}_dm"
    fi

    for g in "${TASK_GRANULARITY[@]}"
    do
        for t in "${N_THREADS[@]}"
        do
            echo "Running experiments for ${exec_version} and granularity ${g} and n_threads=${t}"
            export OMP_NUM_THREADS=$t
            export MIN_LOCAL_TASKS_IN_QUEUE_BEFORE_MIGRATION=$t
            for r in {1..${N_REPETITIONS}}
            do
                eval "${MPI_EXEC_CMD} -np ${N_PROCS} ${MPI_EXPORT_VARS} ${CMD_VTUNE_PREFIX} ${DIR_MXM_EXAMPLE}/main $g ${MXM_PARAMS}" &> ${DIR_RESULT}/results_${exec_version}_${g}_${t}t_${r}.log
            done
        done
    done
}

# =============== Multi task offloading
# make clean -C ${DIR_CH_SRC}
# TARGET=claix_intel INSTALL_DIR=~/install/chameleon-lib/intel_1.0 make -C ${DIR_CH_SRC}
# # build matrix example once
# make clean -C ${DIR_MXM_EXAMPLE}
# ITERATIVE_VERSION=0 make -C ${DIR_MXM_EXAMPLE}
run_experiments "multi"

# =============== Only single task is offloaded
export MAX_TASKS_PER_RANK_TO_MIGRATE_AT_ONCE=1
run_experiments "single"

# # =============== Multi task offloading
# export MAX_TASKS_PER_RANK_TO_MIGRATE_AT_ONCE=30
# make clean -C ${DIR_CH_SRC}
# TARGET=claix_intel INSTALL_DIR=~/install/chameleon-lib/intel_1.0 CUSTOM_COMPILE_FLAGS='-DOFFLOAD_SEND_TASKS_SEPARATELY=1' make -C ${DIR_CH_SRC}
# run_experiments "separate"