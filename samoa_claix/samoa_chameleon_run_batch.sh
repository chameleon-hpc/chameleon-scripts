#!/usr/local_rwth/bin/zsh
##SBATCH --job-name=samoa_chameleon
##SBATCH --output=output_samoa_chameleon.%J.txt
#SBATCH --time=00:10:00
##SBATCH --hwctr=likwid
#SBATCH --partition=c18m
#SBATCH --account=thes0986

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
export NUM_SECTIONS=${NUM_SECTIONS:-25}
export DMIN=${DMIN:-17}
export DMAX=${DMAX:-24}
export NUM_STEPS=${NUM_STEPS:-100}
export SIM_TIME_SEC=${SIM_TIME_SEC:-120}
export SIM_LIMIT="-nmax ${NUM_STEPS}"
#export SIM_LIMIT="-tmax ${SIM_TIME_SEC}"
export ASAGI_PARAMS="${ASAGI_PARAMS:-"-fbath /path/to/bath.nc -fdispl /path/to/displ.nc"}"
# export ASAGI_PARAMS=""

# ===== set core environment ======
source samoa_core_env.sh

# ===== MPI / OpenMP Settings =====
export OMP_PLACES=cores
# export OMP_PROC_BIND=close #? Why did he choose close?
export OMP_PROC_BIND=spread
export ORIG_OMP_NUM_THREADS=${ORIG_OMP_NUM_THREADS:-4}
export CUR_MPI_CMD="${MPIEXEC} ${FLAGS_MPI_BATCH} --export=${ENVS_FOR_EXPORT}"
export MIN_ABS_LOAD_IMBALANCE_BEFORE_MIGRATION=$((ORIG_OMP_NUM_THREADS*1.3))
# export CUR_MPI_CMD="mpiexec.hydra -n 2 -genvall"

# ====== Chameleon Settings =======
export CHAM_AFF_TASK_SELECTION_STRAT=1      # ALL_LINEAR
export CHAM_AFF_PAGE_SELECTION_STRAT=2      # EVERY_NTH
export CHAM_AFF_PAGE_WEIGHTING_STRAT=2      # BY_SIZE
export CHAM_AFF_CONSIDER_TYPES=1            # ONLY TO
export CHAM_AFF_PAGE_SELECTION_N=16         # every 16th
export CHAM_AFF_TASK_SELECTION_N=3          # (not used)
export CHAM_AFF_MAP_MODE=3                  # COMBINED_MODE
export CHAM_AFF_ALWAYS_CHECK_PHYSICAL=1     # recheck every time

# export CHAMELEON_VERSION="chameleon/intel_no_affinity"
# export CHAM_SETTINGS_STR="no_affinity" #for naming the result file


# 0: no chameleon
# 1: chameleon version
# 2: no chameleon but same packing methods required to run chameleon (fair comparison)
# CHAMELEON_VALUES=(0 1 2)
CHAMELEON_VALUES=(1)

# time steps after which CCP will happen
LB_FREQ=(1000000)

# ============================================================
# ===== Run
# ============================================================
# create result directory
mkdir -p ${CUR_OUTP_STR}


run_samoa_experiment() {
    # CUR_DIR=$(pwd)
    
    if [ "${RUN_TRACE}" = "1" ]; then   #! Trace
        export VT_LOGFILE_PREFIX=${CUR_DIR}/Tracing/trace_${TEST_NAME}
        export VT_FLUSH_PREFIX=${VT_LOGFILE_PREFIX}
        mkdir -p ${VT_LOGFILE_PREFIX}
        cd ${VT_LOGFILE_PREFIX}    
    fi
    
    export RES_NAME="${CHAM_SETTINGS_STR}_${EXE_NAME}_thr_${OMP_NUM_THREADS}_dmin_${DMIN}_dmax_${DMAX}_lbfreq_${cur_lb}.log"
    export RES_PATH="${CUR_DIR}/${CUR_OUTP_STR}/${RES_NAME}"
    echo "${CUR_MPI_CMD} ${SAMOA_VTUNE_PREFIX} ${SAMOA_BIN_DIR}/${EXE_NAME} ${NEW_SAMOA_PARAMS} &> ${RES_PATH}"
    ${CUR_MPI_CMD} ${SAMOA_VTUNE_PREFIX} ${SAMOA_BIN_DIR}/${EXE_NAME} ${NEW_SAMOA_PARAMS} &> ${RES_PATH}
    
    cd ${CUR_DIR}
}

run_experiment(){
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
}

printEnv(){
    module list
    env
}

#########################################################
#                       Tests                           #
#########################################################
export GROUP_INDEX=-1
for nSteps in 50 #10 50 100 250 500 1000
do
export NUM_STEPS=${nSteps}
export SIM_LIMIT="-nmax ${NUM_STEPS}"
source samoa_core_env.sh
export GROUP_INDEX=$(($GROUP_INDEX+1))    # for plotting
export SOME_INDEX=-1

# #* No affinity
# export SOME_INDEX=$(($SOME_INDEX+1))    # for plotting
# export CHAMELEON_VERSION="chameleon/intel_no_affinity"
# export CHAM_SETTINGS_STR="${NUM_STEPS}_no_affinity" #for naming the result file
# source samoa_load_modules.sh
# run_experiment
# printEnv &>> ${RES_PATH} # print affinity settings, etc. in log file

#* default affinity (checks a lot of tasks physically)
export SOME_INDEX=$(($SOME_INDEX+1))    # for plotting
export CHAM_AFF_TASK_SELECTION_STRAT=1      # all-linear
export CHAM_AFF_PAGE_SELECTION_STRAT=2      # every n-th
export CHAM_AFF_PAGE_WEIGHTING_STRAT=2      # BY_SIZE
export CHAM_AFF_CONSIDER_TYPES=1            # CONSIDER-TO
export CHAM_AFF_PAGE_SELECTION_N=16         # PageN
export CHAM_AFF_TASK_SELECTION_N=3         # TaskN
export CHAM_AFF_MAP_MODE=3                  # COMBINED_MODE
export CHAM_AFF_ALWAYS_CHECK_PHYSICAL=1     # recheck every time
export CHAMELEON_VERSION="chameleon/intel"
export CHAM_SETTINGS_STR="${NUM_STEPS}_affinity_default" #for naming the result file
source samoa_load_modules.sh
run_experiment
printEnv &>> ${RES_PATH} # print affinity settings, etc. in log file

# #* default affinity but with consider-all
# export SOME_INDEX=$(($SOME_INDEX+1))    # for plotting
# export CHAM_AFF_TASK_SELECTION_STRAT=1      # all-linear
# export CHAM_AFF_PAGE_SELECTION_STRAT=2      # every n-th
# export CHAM_AFF_PAGE_WEIGHTING_STRAT=2      # BY_SIZE
# export CHAM_AFF_PAGE_SELECTION_N=16         # PageN
# export CHAM_AFF_TASK_SELECTION_N=3         # TaskN
# export CHAM_AFF_MAP_MODE=3                  # COMBINED_MODE
# export CHAM_AFF_ALWAYS_CHECK_PHYSICAL=1     # recheck every time
# export CHAM_AFF_CONSIDER_TYPES=0            # CONSIDER ALL
# export CHAMELEON_VERSION="chameleon/intel"
# export CHAM_SETTINGS_STR="${NUM_STEPS}_affinity_ConsiderAll" #for naming the result file
# source samoa_load_modules.sh
# run_experiment
# printEnv &>> ${RES_PATH} # print affinity settings, etc. in log file

# #* affinity checking less tasks and pages
# export SOME_INDEX=$(($SOME_INDEX+1))    # for plotting
# export CHAM_AFF_TASK_SELECTION_STRAT=3      # N_EQS
# export CHAM_AFF_PAGE_SELECTION_STRAT=8      # middle
# export CHAM_AFF_PAGE_WEIGHTING_STRAT=2      # BY_SIZE
# export CHAM_AFF_CONSIDER_TYPES=0            # CONSIDER-ALL
# export CHAM_AFF_PAGE_SELECTION_N=16         # PageN
# export CHAM_AFF_TASK_SELECTION_N=16         # TaskN
# export CHAM_AFF_MAP_MODE=3                  # COMBINED_MODE
# export CHAM_AFF_ALWAYS_CHECK_PHYSICAL=0     # dont recheck every time
# export CHAMELEON_VERSION="chameleon/intel"
# export CHAM_SETTINGS_STR="${NUM_STEPS}_affinity_16EQS_Middle_Con-All_No-AlChPh" #for naming the result file
# source samoa_load_modules.sh
# run_experiment
# printEnv &>> ${RES_PATH} # print affinity settings, etc. in log file

# #* affinity domain mode checking less tasks and pages
# export SOME_INDEX=$(($SOME_INDEX+1))    # for plotting
# export CHAM_AFF_TASK_SELECTION_STRAT=3      # N_EQS
# export CHAM_AFF_PAGE_SELECTION_STRAT=8      # middle
# export CHAM_AFF_PAGE_WEIGHTING_STRAT=2      # BY_SIZE
# export CHAM_AFF_CONSIDER_TYPES=0            # CONSIDER-ALL
# export CHAM_AFF_PAGE_SELECTION_N=16         # PageN
# export CHAM_AFF_TASK_SELECTION_N=16         # TaskN
# export CHAM_AFF_MAP_MODE=0                  # DOMAIN_MODE
# export CHAM_AFF_ALWAYS_CHECK_PHYSICAL=0     # dont recheck every time
# export CHAMELEON_VERSION="chameleon/intel"
# export CHAM_SETTINGS_STR="${NUM_STEPS}_affinity_DomainMode_16EQS_Middle" #for naming the result file
# source samoa_load_modules.sh
# run_experiment
# printEnv &>> ${RES_PATH} # print affinity settings, etc. in log file

# #* affinity enabled but no tasks checked, only initial location calculation
# export SOME_INDEX=$(($SOME_INDEX+1))    # for plotting
# export CHAM_AFF_TASK_SELECTION_STRAT=0      # NONE
# export CHAM_AFF_PAGE_SELECTION_STRAT=8      # middle
# export CHAM_AFF_PAGE_WEIGHTING_STRAT=2      # BY_SIZE
# export CHAM_AFF_CONSIDER_TYPES=0            # CONSIDER-ALL
# export CHAM_AFF_PAGE_SELECTION_N=16         # PageN
# export CHAM_AFF_TASK_SELECTION_N=16         # TaskN
# export CHAM_AFF_MAP_MODE=0                  # DOMAIN_MODE
# export CHAM_AFF_ALWAYS_CHECK_PHYSICAL=0     # dont recheck every time
# export CHAMELEON_VERSION="chameleon/intel"
# export CHAM_SETTINGS_STR="${NUM_STEPS}_affinity_NONE_MiddlePage" #for naming the result file
# source samoa_load_modules.sh
# run_experiment
# printEnv &>> ${RES_PATH} # print affinity settings, etc. in log file

# #* affinity enabled but no tasks checked, initial location calc minimized
# export SOME_INDEX=$(($SOME_INDEX+1))    # for plotting
# export CHAM_AFF_TASK_SELECTION_STRAT=0      # NONE
# export CHAM_AFF_PAGE_SELECTION_STRAT=0      # first-of-first only
# export CHAM_AFF_PAGE_WEIGHTING_STRAT=0      # first only
# export CHAM_AFF_CONSIDER_TYPES=0            # CONSIDER-ALL
# export CHAM_AFF_PAGE_SELECTION_N=16         # PageN
# export CHAM_AFF_TASK_SELECTION_N=16         # TaskN
# export CHAM_AFF_MAP_MODE=0                  # DOMAIN_MODE
# export CHAM_AFF_ALWAYS_CHECK_PHYSICAL=0     # dont recheck every time
# export CHAMELEON_VERSION="chameleon/intel"
# export CHAM_SETTINGS_STR="${NUM_STEPS}_affinity_NONE_FirstOfFirstPage" #for naming the result file
# source samoa_load_modules.sh
# run_experiment
# printEnv &>> ${RES_PATH} # print affinity settings, etc. in log file

echo "finished NUM_STEPS=${NUM_STEPS}\n"
done # NUM_STEPS

squeue -u ka387454 # get total runtime of the job