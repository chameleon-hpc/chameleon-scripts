#!/usr/local_rwth/bin/zsh
#SBATCH --job-name=samoa_chameleon
#SBATCH --output=output_samoa_chameleon.%J.txt
#SBATCH --time=02:30:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=24
#SBATCH --partition=c18m
#SBATCH --hwctr=likwid

# ============================================================
# ===== Loading Modules
# ============================================================
source ./samoa_load_modules.sh

# ============================================================
# ===== Parameters
# ============================================================
export SAMOA_DIR="${SAMOA_DIR:-"/path/to/samoa_chameleon"}"
export SAMOA_OUTPUT_DIR="${SAMOA_OUTPUT_DIR:-"/path/to/samoa_output"}"
export CHAMELEON_TOOL_LIBRARIES="${CHAMELEON_TOOL_LIBRARIES:-""}"
export SAMOA_BIN_DIR=${SAMOA_DIR}/bin

export RUN_RADIAL=${RUN_RADIAL:-1}
export RUN_OSCILL=${RUN_OSCILL:-1}
export RUN_ASAGI=${RUN_ASAGI:-1}
export RUN_TRACE=${RUN_TRACE:-0}

# ===== Simulation Settings =====
export NUM_SECTIONS=${NUM_SECTIONS:-20}
export DMIN=${DMIN:-17}
export DMAX=${DMAX:-24}
export NUM_STEPS=${NUM_STEPS:-100}
export SIM_TIME_SEC=${SIM_TIME_SEC:-3600}
export SIM_LIMIT="-nmax ${NUM_STEPS}"
# export SIM_LIMIT="-tmax ${SIM_TIME_SEC}"
export ASAGI_PARAMS="${ASAGI_PARAMS:-"-fbath /path/to/bath.nc -fdispl /path/to/displ.nc"}"
# export ASAGI_PARAMS=""

# ===== set core environment ======
source samoa_core_env.sh

# ===== MPI / OpenMP Settings =====
export OMP_PLACES=cores
export OMP_PROC_BIND=close
export ORIG_OMP_NUM_THREADS=${ORIG_OMP_NUM_THREADS:-4}
export CUR_MPI_CMD="${MPIEXEC} ${FLAGS_MPI_BATCH} --export=${ENVS_FOR_EXPORT}"
export MIN_ABS_LOAD_IMBALANCE_BEFORE_MIGRATION=$((ORIG_OMP_NUM_THREADS))
# export CUR_MPI_CMD="mpiexec.hydra -n 2 -genvall"

# 0: no chameleon
# 1: chameleon version
# 2: no chameleon but same packing methods required to run chameleon (fair comparison)
CHAMELEON_VALUES=(0 1 2)

# time steps after which CCP will happen
LB_FREQ=(1000000)

# ============================================================
# ===== Run
# ============================================================
# create result directory
mkdir -p ${CUR_OUTP_STR}

run_samoa_experiment() {
    CUR_DIR=$(pwd)
    
    if [ "${RUN_TRACE}" = "1" ]; then
        export VT_LOGFILE_PREFIX=trace_${EXE_NAME}
        export VT_FLUSH_PREFIX=${VT_LOGFILE_PREFIX}
        mkdir -p ${VT_LOGFILE_PREFIX}
        cd ${VT_LOGFILE_PREFIX}    
    fi
    
    echo "${CUR_MPI_CMD} ${SAMOA_VTUNE_PREFIX} ${SAMOA_BIN_DIR}/${EXE_NAME} ${NEW_SAMOA_PARAMS} &> ${CUR_DIR}/${CUR_OUTP_STR}/${EXE_NAME}_thr_${OMP_NUM_THREADS}_dmin_${DMIN}_dmax_${DMAX}_lbfreq_${cur_lb}.log"
    ${CUR_MPI_CMD} ${SAMOA_VTUNE_PREFIX} ${SAMOA_BIN_DIR}/${EXE_NAME} ${NEW_SAMOA_PARAMS} &> ${CUR_DIR}/${CUR_OUTP_STR}/${EXE_NAME}_thr_${OMP_NUM_THREADS}_dmin_${DMIN}_dmax_${DMAX}_lbfreq_${cur_lb}.log
    
    cd ${CUR_DIR}
}

for cur_lb in "${LB_FREQ[@]}"
do
    # append LB freq for run
    export NEW_SAMOA_PARAMS="${SAMOA_PARAMS} -lbfreq ${cur_lb}"

    for cur_ch in "${CHAMELEON_VALUES[@]}"
    do
        if [ "${cur_ch}" = "1" ]; then
            export OMP_NUM_THREADS=${ORIG_OMP_NUM_THREADS}
            # export OMP_NUM_THREADS=$((ORIG_OMP_NUM_THREADS-1))
        else
            export OMP_NUM_THREADS=${ORIG_OMP_NUM_THREADS}
        fi

        if [ "${RUN_RADIAL}" = "1" ]; then
            EXE_NAME="samoa_swe_radial_chameleon_${cur_ch}"
            run_samoa_experiment
        fi

        if [ "${RUN_OSCILL}" = "1" ]; then
            EXE_NAME="samoa_swe_oscillating_chameleon_${cur_ch}"
            run_samoa_experiment
        fi

        if [ "${RUN_ASAGI}" = "1" ]; then
            EXE_NAME="samoa_swe_asagi_chameleon_${cur_ch}"
            run_samoa_experiment
        fi
    done
done
