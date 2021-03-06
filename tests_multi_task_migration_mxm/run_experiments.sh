#!/usr/local_rwth/bin/zsh
#SBATCH --time=12:00:00
#SBATCH --exclusive
#SBATCH --account=jara0001
#SBATCH --partition=c16m

# =============== Load desired modules
source ~/.zshrc
source env_ch_intel.sh
module unload chameleon-lib

# # hack because currently vtune is not supported in batch usage
# module load c_vtune
# export CMD_VTUNE_PREFIX="amplxe-cl –collect hotspots –r ./${CUR_DATE_STR}_profiling_chameleon_${OMP_NUM_THREADS}t -trace-mpi -- "

# =============== Settings & environment variables
IS_DISTRIBUTED=${IS_DISTRIBUTED:-1}
IS_SEPARATE=${IS_SEPARATE:-0}
N_PROCS=${N_PROCS:-2}
N_REPETITIONS=${N_REPETITIONS:-10}
CUR_DATE_STR=${CUR_DATE_STR:-"$(date +"%Y%m%d_%H%M%S")"}

TASK_GRANULARITY=(50 100 150 200 250 300 350 400 450 500 550 600)
# default number of threads for distributed runs
N_THREADS=(2 4 6 8 10 12 14 16 18 20 22)

# create result directory
if [ "${IS_DISTRIBUTED}" = "1" ]; then
    export SUFFIX_RESULT_DIR="dm"
else
    export SUFFIX_RESULT_DIR="sm"
fi

DIR_RESULT="${CUR_DATE_STR}_results/${N_PROCS}procs_${SUFFIX_RESULT_DIR}"
DIR_MXM_EXAMPLE=${DIR_MXM_EXAMPLE:-../../chameleon-apps/applications/matrix_example}
mkdir -p ${DIR_RESULT}

if [ "${IS_SEPARATE}" = "1" ]; then
  # set env vars to use lib
  export LD_LIBRARY_PATH="${DIR_CH_SEPARATE_INSTALL}/lib:${LD_LIBRARY_PATH}"
  export LIBRARY_PATH="${DIR_CH_SEPARATE_INSTALL}/lib:${LIBRARY_PATH}"
  export INCLUDE="${DIR_CH_SEPARATE_INSTALL}/include:${INCLUDE}"
  export CPATH="${DIR_CH_SEPARATE_INSTALL}/include:${CPATH}"
else
# set env vars to use lib
  export LD_LIBRARY_PATH="${DIR_CH_REGULAR_INSTALL}/lib:${LD_LIBRARY_PATH}"
  export LIBRARY_PATH="${DIR_CH_REGULAR_INSTALL}/lib:${LIBRARY_PATH}"
  export INCLUDE="${DIR_CH_REGULAR_INSTALL}/include:${INCLUDE}"
  export CPATH="${DIR_CH_REGULAR_INSTALL}/include:${CPATH}"
fi

case ${N_PROCS} in
    2)
        echo "Running with 2 procs"
        MXM_PARAMS="2400 0"
        if [ "${IS_DISTRIBUTED}" = "0" ]; then
            N_THREADS=(1 2 3 4 5 6 7 8 9 10 11)
        fi
        ;;
    4)
        echo "Running with 4 procs"
        MXM_PARAMS="2400 1600 800 0"
        if [ "${IS_DISTRIBUTED}" = "0" ]; then
            N_THREADS=(1 2 3 4 5)
        fi
        ;;
    8)
        echo "Running with 8 procs"
        MXM_PARAMS="2400 2057 1714 1371 1028 685 342 0"
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
export MAX_TASKS_PER_RANK_TO_MIGRATE_AT_ONCE=15
export PERCENTAGE_DIFF_TASKS_TO_MIGRATE=0.3

# load flags
source ../../chameleon/flags_claix_intel.def

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

if [ "${IS_SEPARATE}" = "1" ]; then
    run_experiments "separate"
else
    run_experiments "multi"
    export MAX_TASKS_PER_RANK_TO_MIGRATE_AT_ONCE=1
    run_experiments "single"
fi
