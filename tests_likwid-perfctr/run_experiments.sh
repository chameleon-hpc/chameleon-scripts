#!/usr/local_rwth/bin/zsh
#SBATCH --time=01:00:00
#SBATCH --exclusive
#SBATCH --partition=c18m
#SBATCH --hwctr=likwid

# =============== Load desired modules
source ~/.zshrc
module load chameleon

# =============== Settings & environment variables
N_PROCS=${N_PROCS:-2}
IS_IMBALANCED=${IS_IMBALANCED:-0}
RUN_LIKWID=${RUN_LIKWID:-1}
N_REPETITIONS=${N_REPETITIONS:-1}
CUR_DATE_STR=${CUR_DATE_STR:-"$(date +"%Y%m%d_%H%M%S")"}
EXE_NAME=${EXE_NAME:-"matrix_app.exe"}

TASK_GRANULARITY=(300)
N_THREADS=(8)

case ${N_PROCS} in
    2)
        echo "Running with 2 procs"
        if [ "${IS_IMBALANCED}" = "1" ]; then
            MXM_PARAMS="1200 0"
        else
            MXM_PARAMS="600 600"
        fi
        ;;
    4)
        echo "Running with 4 procs"
        if [ "${IS_IMBALANCED}" = "1" ]; then
            MXM_PARAMS="1200 800 400 0"
        else
            MXM_PARAMS="600 600 600 600"
        fi
        ;;
    *)
        echo "Unsupported number of procs"
        exit
        ;;
    esac

DIR_RESULT="${CUR_DATE_STR}_results/imb${IS_IMBALANCED}_${N_PROCS}procs_${SLURM_NTASKS_PER_NODE}pernode"
DIR_MXM_EXAMPLE=${DIR_MXM_EXAMPLE:-../../chameleon-apps/applications/matrix_example}
mkdir -p ${DIR_RESULT}

# export necessary stuff that is used in wrapper script
export EXE_NAME
export DIR_MXM_EXAMPLE
export MXM_PARAMS
export RUN_LIKWID

export MIN_REL_LOAD_IMBALANCE_BEFORE_MIGRATION=0.1
export MAX_TASKS_PER_RANK_TO_MIGRATE_AT_ONCE=1
export PERCENTAGE_DIFF_TASKS_TO_MIGRATE=0.3
export MPI_EXEC_CMD="${RUN_SETTINGS_SLURM} ${MPIEXEC} ${FLAGS_MPI_BATCH}"

for nt in "${N_THREADS[@]}"
do
    export OMP_NUM_THREADS=${nt}
    export MIN_LOCAL_TASKS_IN_QUEUE_BEFORE_MIGRATION=${nt}

    for g in "${TASK_GRANULARITY[@]}"
    do
        echo "Running experiments for granularity ${g} and n_threads=${nt}"
        export GRANU=${g}
        for r in {1..${N_REPETITIONS}}
        do
            export TMP_NAME_RUN="${DIR_RESULT}/results_${g}_${nt}t_${r}"
            eval "${MPI_EXEC_CMD} ${MPI_EXPORT_VARS_SLURM} ./wrapper.sh" &> ${TMP_NAME_RUN}.log
        done
    done
done
