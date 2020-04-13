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
DIR_SAMOA=${DIR_SAMOA:-../../samoa-chameleon}
SAMOA_EXE_NAME=${SAMOA_EXE_NAME:-samoa_swe_packing}
SAMOA_OUT_DIR=${SAMOA_OUT_DIR:-.}

export TOHOKU_PARAMS="-fbath /work/jk869269/repos/chameleon/samoa_data/tohoku_static/bath.nc -fdispl /work/jk869269/repos/chameleon/samoa_data/tohoku_static/displ.nc"
export NUM_SECTIONS=16
export CUR_DMIN=15
export CUR_DMAX=25
export NUM_STEPS=150
export SIM_TIME_SEC=3600
export LB_STEPS=5000
export SAMOA_PARAMS=" -output_dir ${SAMOA_OUT_DIR} -lbthreshold 0.1 -dmin ${CUR_DMIN} -dmax ${CUR_DMAX} -sections ${NUM_SECTIONS} -tmax ${SIM_TIME_SEC} ${TOHOKU_PARAMS}"

# # hack because currently vtune is not supported in batch usage
# module load c_vtune
# export CMD_VTUNE_PREFIX="amplxe-cl –collect hotspots –r ./${CUR_DATE_STR}_profiling_chameleon_${OMP_NUM_THREADS}t -trace-mpi -- "

echo "===== Resetting power caps and CPU frequencies of all machines (${N_NODES} nodes)"
zsh ./hardware_manipulation/reset_all.sh ${N_NODES}

DIR_RESULT="results_experiment5"
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

echo "===== Running experiment 5 for ${current_name}, n_threads=${tmp_n_threads} - sam(oa)^2 without CCP"
for rep in {1..${N_REPETITIONS}}
do
    TMP_FILE_NAME="${DIR_RESULT}/results_${current_name}_${N_NODES}nodes_${tmp_n_threads}thr_${rep}"
    python3.6 ../../utils/powermeter/power_client.py -p 0.1 -t -C -o ${TMP_FILE_NAME}_power.log "${MPI_EXEC_CMD} ${MPI_EXPORT_VARS_SLURM},SAMOA_PARAMS ${CMD_VTUNE_PREFIX} ${DIR_SAMOA}/bin/${SAMOA_EXE_NAME} ${SAMOA_PARAMS} -lbfreq 100000000 &> ${TMP_FILE_NAME}.log"
done

echo "===== Running experiment 5 for ${current_name}, n_threads=${tmp_n_threads} - sam(oa)^2 with CCP"
for rep in {1..${N_REPETITIONS}}
do
    TMP_FILE_NAME="${DIR_RESULT}/results_${current_name}_${N_NODES}nodes_${tmp_n_threads}thr_ccp_${rep}"
    python3.6 ../../utils/powermeter/power_client.py -p 0.1 -t -C -o ${TMP_FILE_NAME}_power.log "${MPI_EXEC_CMD} ${MPI_EXPORT_VARS_SLURM},SAMOA_PARAMS ${CMD_VTUNE_PREFIX} ${DIR_SAMOA}/bin/${SAMOA_EXE_NAME} ${SAMOA_PARAMS} -lbfreq ${LB_STEPS} &> ${TMP_FILE_NAME}.log"
done
