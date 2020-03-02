#!/usr/local_rwth/bin/zsh
#SBATCH --time=12:00:00
#SBATCH --exclusive
#SBATCH --account=jara0001
#SBATCH --partition=c16m

# =============== Load desired modules
source ~/.zshrc
source env_ch_intel.sh
module unload chameleon-lib

export ORIG_LD_LIBRARY_PATH="${LD_LIBRARY_PATH}"
export ORIG_LIBRARY_PATH="${LIBRARY_PATH}"
export ORIG_INCLUDE="${INCLUDE}"
export ORIG_CPATH="${CPATH}"

# # hack because currently vtune is not supported in batch usage
# module load c_vtune
# export CMD_VTUNE_PREFIX="amplxe-cl –collect hotspots –r ./${CUR_DATE_STR}_profiling_chameleon_${OMP_NUM_THREADS}t -trace-mpi -- "

# =============== Settings & environment variables
IS_DISTRIBUTED=${IS_DISTRIBUTED:-1}
N_PROCS=${N_PROCS:-2}
N_REPETITIONS=${N_REPETITIONS:-2}
CUR_DATE_STR=${CUR_DATE_STR:-"$(date +"%Y%m%d_%H%M%S")"}
FULL_NR_THREADS=${FULL_NR_THREADS:-24}

# TASK_GRANULARITY=(50 100 150 200 250 300 350 400 450 500 550 600)
TASK_GRANULARITY=(50 250)

# create result directory
if [ "${IS_DISTRIBUTED}" = "1" ]; then
    export SUFFIX_RESULT_DIR="dm"
else
    export SUFFIX_RESULT_DIR="sm"
fi

DIR_RESULT="${CUR_DATE_STR}_results/${N_PROCS}procs_${SUFFIX_RESULT_DIR}"
DIR_MXM_EXAMPLE=${DIR_MXM_EXAMPLE:-../../chameleon-apps/applications/matrix_example}
mkdir -p ${DIR_RESULT}

case ${N_PROCS} in
    2)
        echo "Running with 2 procs"
        MXM_PARAMS="2400 0"
        ;;
    4)
        echo "Running with 4 procs"
        MXM_PARAMS="2400 1600 800 0"
        ;;
    8)
        echo "Running with 8 procs"
        MXM_PARAMS="2400 2057 1714 1371 1028 685 342 0"
        ;;
    *)
        echo "ERROR: Sorry script does not support number of threads. Aborting here"
        exit 2
    esac

echo "Setting initial env vars"
export MIN_REL_LOAD_IMBALANCE_BEFORE_MIGRATION=0.1
export MAX_TASKS_PER_RANK_TO_MIGRATE_AT_ONCE=1
export PERCENTAGE_DIFF_TASKS_TO_MIGRATE=0.3

echo "Loading compiler flags"
# load flags
source ../../chameleon/flags_claix_intel.def

echo "Determine MPI Command"
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
        echo "Running experiments for ${exec_version} and granularity ${g} and n_threads=$2"
        export OMP_NUM_THREADS=$2
        export MIN_LOCAL_TASKS_IN_QUEUE_BEFORE_MIGRATION=$2
        for r in {1..${N_REPETITIONS}}
        do
            eval "${MPI_EXEC_CMD} -np ${N_PROCS} ${MPI_EXPORT_VARS} ${CMD_VTUNE_PREFIX} ${DIR_MXM_EXAMPLE}/main $g ${MXM_PARAMS}" &> ${DIR_RESULT}/results_${exec_version}_${g}_${N_PROCS}procs_$2t_${r}.log
        done
    done
}

for VAR in 0 1 2 3 4
do
    echo "Running tests for communication mode ${VAR}"
    name_install="DIR_CH_MODE${VAR}_INSTALL"
    eval cur_install=\$${name_install}
    tmp_n_threads=${FULL_NR_THREADS}
    if [[ "${VAR}" == "0" ]]; then
        tmp_n_threads=$((FULL_NR_THREADS-1))
    fi
    if [[ "${VAR}" == "3" ]]; then
        tmp_n_threads=$((FULL_NR_THREADS-1))
    fi
    # set env vars to use lib
    export LD_LIBRARY_PATH="${cur_install}/lib:${ORIG_LD_LIBRARY_PATH}"
    export LIBRARY_PATH="${cur_install}/lib:${ORIG_LIBRARY_PATH}"
    export INCLUDE="${cur_install}/include:${ORIG_INCLUDE}"
    export CPATH="${cur_install}/include:${ORIG_CPATH}"

    run_experiments "mode${VAR}" "${tmp_n_threads}"
done