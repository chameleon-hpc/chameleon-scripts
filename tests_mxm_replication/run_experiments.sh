#!/bin/bash
#SBATCH --time=08:00:00
#SBATCH --exclusive
#SBATCH --account=pr48ma
#SBATCH --partition=micro
#SBATCH --ear=off

module list


# =============== Settings & environment variables
N_PROCS=${N_PROCS:-2}
N_REPETITIONS=${N_REPETITIONS:-10}
CUR_DATE_STR=${CUR_DATE_STR:-"$(date +"%Y%m%d_%H%M%S")"}

#TASK_GRANULARITY=(50 100 150 200 250 300 350 400 450 500 550 600)
TASK_GRANULARITY=(100 150 200 250 300 350 400 450 500 550 600)
# default number of threads for distributed runs
N_THREADS=(2 4 6 8 10 12 14 16 18 20 22)

# create result directory

LOAD=1000
DIR_RESULT="${CUR_DATE_STR}_results_${LOAD}_${REP_MODE}/${N_PROCS}procs_rep_${REP_MODE}"
DIR_MXM_EXAMPLE=${DIR_MXM_EXAMPLE:-../../chameleon-apps/applications/matrix_example}
mkdir -p ${DIR_RESULT}


case ${REP_MODE} in 
  0) 
    export CHAM_INSTALL_DIR=${DIR_CH_REP0_INSTALL}
    ;; 
  2)
    export CHAM_INSTALL_DIR=${DIR_CH_REP2_INSTALL}
    ;; 
  3)
    export CHAM_INSTALL_DIR=${DIR_CH_REP3_INSTALL}
    ;; 
  4) 
    export CHAM_INSTALL_DIR=${DIR_CH_REP4_INSTALL}
    ;; 
esac

echo "using installation "${CHAM_INSTALL_DIR}


# set env vars to use lib
export LD_LIBRARY_PATH="${CHAM_INSTALL_DIR}/lib:${LD_LIBRARY_PATH}"
export LIBRARY_PATH="${CHAM_INSTALL_DIR}/lib:${LIBRARY_PATH}"
export INCLUDE="${CHAM_INSTALL_DIR}/include:${INCLUDE}"
export CPATH="${CHAM_INSTALL_DIR}/include:${CPATH}"

ldd ${DIR_MXM_EXAMPLE}/main


case ${N_PROCS} in
    2)
        echo "Running with 2 procs"
        MXM_PARAMS="${LOAD} ${LOAD}"
        ;;
esac

export MIN_REL_LOAD_IMBALANCE_BEFORE_MIGRATION=0.1
export MAX_TASKS_PER_RANK_TO_ACTIVATE_AT_ONCE=100
export PERCENTAGE_DIFF_TASKS_TO_MIGRATE=0.5

# load flags
source ../../chameleon-lib/flags_sng_intel.def

MPI_EXEC_CMD="${RUN_SETTINGS} mpiexec"

# =============== Execution Function
function run_experiments()
{

    for g in "${TASK_GRANULARITY[@]}"
    do
        for t in "${N_THREADS[@]}"
        do
            echo "Running experiments for ${exec_version} and granularity ${g} and n_threads=${t}"
            export OMP_NUM_THREADS=$t
            export MIN_LOCAL_TASKS_IN_QUEUE_BEFORE_MIGRATION=$t
            for r in `seq 1 ${N_REPETITIONS}`
            do
                export MAX_PERCENTAGE_REPLICATED_TASKS=0.1
                echo "${MPI_EXEC_CMD} -np ${N_PROCS} ${MPI_EXPORT_VARS} ${DIR_MXM_EXAMPLE}/main $g ${MXM_PARAMS}" 
                mpiexec ./wrapper_sudden_dist.sh 1.2 0 0  "${DIR_MXM_EXAMPLE}/main" "$g ${MXM_PARAMS}" &> ${DIR_RESULT}/results_0.1_${g}_${t}t_${r}.log
                export MAX_PERCENTAGE_REPLICATED_TASKS=0.5
                echo "${MPI_EXEC_CMD} -np ${N_PROCS} ${MPI_EXPORT_VARS} ${DIR_MXM_EXAMPLE}/main $g ${MXM_PARAMS}" 
                mpiexec ./wrapper_sudden_dist.sh 1.2 0 0  "${DIR_MXM_EXAMPLE}/main" "$g ${MXM_PARAMS}" &> ${DIR_RESULT}/results_0.5_${g}_${t}t_${r}.log
                export MAX_PERCENTAGE_REPLICATED_TASKS=0.0
                echo "${MPI_EXEC_CMD} -np ${N_PROCS} ${MPI_EXPORT_VARS} ${DIR_MXM_EXAMPLE}/main $g ${MXM_PARAMS}" 
                mpiexec ./wrapper_sudden_dist.sh 1.2 0 0  "${DIR_MXM_EXAMPLE}/main" "$g ${MXM_PARAMS}" &> ${DIR_RESULT}/results_0.0_${g}_${t}t_${r}.log
            done
        done
    done
}

run_experiments 
