#!/usr/local_rwth/bin/zsh
#SBATCH --time=12:00:00
#SBATCH --exclusive
#SBATCH --partition=c16m
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=24
#SBATCH --account=rwth0548
#SBATCH --reservation=rwth0548

# =============== Load desired modules
source ~/.zshrc
source env_ch_intel.sh
module unload chameleon-lib

export ORIG_LD_LIBRARY_PATH="${LD_LIBRARY_PATH}"
export ORIG_LIBRARY_PATH="${LIBRARY_PATH}"
export ORIG_INCLUDE="${INCLUDE}"
export ORIG_CPATH="${CPATH}"

# =============== Settings & environment variables
N_NODES=${N_NODES:-1}
N_REPETITIONS=${N_REPETITIONS:-5}
CUR_DATE_STR=${CUR_DATE_STR:-"$(date +"%Y%m%d_%H%M%S")"}
FULL_NR_THREADS=${FULL_NR_THREADS:-24}
IS_CHAMELEON=${IS_CHAMELEON:-0}
MXM_PROG_NAME=${MXM_PROG_NAME:-main}

TASK_GRANULARITY=(600)
NUM_TASKS=3200
# ARRAY_POWERCAP=(105 100 95 90 85 80 75 70 65 60 55)
ARRAY_POWERCAP=(105 100)

# # hack because currently vtune is not supported in batch usage
# module load c_vtune
# export CMD_VTUNE_PREFIX="amplxe-cl –collect hotspots –r ./${CUR_DATE_STR}_profiling_chameleon_${OMP_NUM_THREADS}t -trace-mpi -- "

echo "===== Resetting power caps and CPU frequencies of all machines (${N_NODES} nodes)"
zsh ./hardware_manipulation/reset_all.sh ${N_NODES}

DIR_RESULT="results_experiment1"
DIR_MXM_EXAMPLE=${DIR_MXM_EXAMPLE:-../../chameleon-apps/applications/matrix_example}
mkdir -p ${DIR_RESULT}

echo "===== Setting initial env vars"
export MIN_REL_LOAD_IMBALANCE_BEFORE_MIGRATION=0.1
export MAX_TASKS_PER_RANK_TO_MIGRATE_AT_ONCE=1
export PERCENTAGE_DIFF_TASKS_TO_MIGRATE=0.3

echo "===== Loading compiler flags"
# load flags
source ../../chameleon/flags_claix_intel.def
MPI_EXEC_CMD="${RUN_SETTINGS_SLURM} ${MPIEXEC} ${FLAGS_MPI_BATCH} "

# set env vars to use lib
export LD_LIBRARY_PATH="${DIR_CH_INSTALL}/lib:${ORIG_LD_LIBRARY_PATH}"
export LIBRARY_PATH="${DIR_CH_INSTALL}/lib:${ORIG_LIBRARY_PATH}"
export INCLUDE="${DIR_CH_INSTALL}/include:${ORIG_INCLUDE}"
export CPATH="${DIR_CH_INSTALL}/include:${ORIG_CPATH}"

if [[ "${IS_CHAMELEON}" == "1" ]]; then
    current_name="chameleon"
    tmp_n_threads=$((FULL_NR_THREADS-1))
else
    current_name="baseline"
    # currently run with less number of threads. strangely running with 24 threads on broadwell results for tasking are worse
    # tmp_n_threads=$((FULL_NR_THREADS))
    tmp_n_threads=$((FULL_NR_THREADS-1))
fi

export OMP_NUM_THREADS=${tmp_n_threads}
export MIN_LOCAL_TASKS_IN_QUEUE_BEFORE_MIGRATION=${tmp_n_threads}

MXM_PARAMS=""
for i_node in {1..${N_NODES}}
do
    MXM_PARAMS="${MXM_PARAMS}${NUM_TASKS} "
done

for gran in "${TASK_GRANULARITY[@]}"
do
    for pc in "${ARRAY_POWERCAP[@]}"
    do
        echo "===== Running experiment 1 for ${current_name}, granularity=${gran}, n_threads=${tmp_n_threads} and powercap=${pc}W"
        zsh ./hardware_manipulation/set_pc_all.sh ${N_NODES} ${pc}

        for rep in {1..${N_REPETITIONS}}
        do
            TMP_FILE_NAME="${DIR_RESULT}/results_${current_name}_${gran}gran_${N_NODES}nodes_${tmp_n_threads}thr_${pc}pc_${rep}"
            python3.6 ../../utils/powermeter/power_client.py -p 0.1 -t -C -o ${TMP_FILE_NAME}_power.log "${MPI_EXEC_CMD} ${MPI_EXPORT_VARS_SLURM} ${CMD_VTUNE_PREFIX} ${DIR_MXM_EXAMPLE}/${MXM_PROG_NAME} ${gran} ${MXM_PARAMS} &> ${TMP_FILE_NAME}.log"
        done
    done
done
