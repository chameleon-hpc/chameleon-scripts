#!/usr/local_rwth/bin/zsh
#SBATCH --time=01:00:00
#SBATCH --exclusive
#SBATCH --account=thes0986
#SBATCH --hwctr=likwid

#########################################################
#               some settings                           #
#########################################################
export CHAM_AFF_TASK_SELECTION_STRAT=1      # ALL_LINEAR
export CHAM_AFF_PAGE_SELECTION_STRAT=2      # EVERY_NTH
export CHAM_AFF_PAGE_WEIGHTING_STRAT=2      # BY_SIZE
export CHAM_AFF_CONSIDER_TYPES=1            # ONLY TO
export CHAM_AFF_PAGE_SELECTION_N=16         # every 16th
export CHAM_AFF_TASK_SELECTION_N=3          # (not used)
export CHAM_AFF_MAP_MODE=3                  # COMBINED_MODE
export CHAM_AFF_ALWAYS_CHECK_PHYSICAL=1     # recheck every time
export AUTOMATIC_NUMA_BALANCING=0           # start with "no_numa_balancing"
export SOME_INDEX=0
export OMP_NUM_THREADS=$((${CPUS_PER_TASK}-1))  # chameleon communication thread
export PROG="mxm_chameleon"
export CHAMELEON_VERSION="chameleon/intel"
export OMP_PLACES=cores 
export OMP_PROC_BIND=close

export N_RUNS=20

LOG_DIR=${OUT_DIR}"/logs"
mkdir -p ${LOG_DIR}

export_vars="CHAMELEON_VERSION,MXM_PARAMS,OMP_NUM_THREADS,CHAM_AFF_TASK_SELECTION_STRAT,CHAM_AFF_PAGE_SELECTION_STRAT,CHAM_AFF_PAGE_WEIGHTING_STRAT,CHAM_AFF_CONSIDER_TYPES,CHAM_AFF_PAGE_SELECTION_N,CHAM_AFF_TASK_SELECTION_N,CHAM_AFF_MAP_MODE,CHAM_AFF_ALWAYS_CHECK_PHYSICAL,NO_NUMA_BALANCING,AUTOMATIC_NUMA_BALANCING,PROG,SOME_INDEX,N_RUNS,RUN_LIKWID"

cd /home/ka387454/repos/chameleon-apps/applications/matrix_example
module use -a /home/ka387454/.modules
module load $CHAMELEON_VERSION

#########################################################
#                   Functions                           #
#########################################################

function run_experiment()
{
# split PARAMS without having to change the extractData.py script...
export MXM_PARAMS="${MXM_SIZE} ${MXM_DISTRIBUTION}"

if [ "$AUTOMATIC_NUMA_BALANCING" -eq "1" ]
then NO_NUMA_BALANCING=""
else NO_NUMA_BALANCING="no_numa_balancing"
fi

hostname
module list
env

echo ""
echo "${MPIEXEC} ${FLAGS_MPI_BATCH}"

OLD_EXPORTS="PATH,CPLUS_INCLUDE_PATH,C_INCLUDE_PATH,CPATH,INCLUDE,LD_LIBRARY_PATH,LIBRARY_PATH,I_MPI_DEBUG,I_MPI_TMI_NBITS_RANK,OMP_NUM_THREADS,OMP_PLACES,OMP_PROC_BIND,KMP_AFFINITY,MIN_ABS_LOAD_IMBALANCE_BEFORE_MIGRATION,MIN_LOCAL_TASKS_IN_QUEUE_BEFORE_MIGRATION,MIN_REL_LOAD_IMBALANCE_BEFORE_MIGRATION,MAX_TASKS_PER_RANK_TO_MIGRATE_AT_ONCE,PERCENTAGE_DIFF_TASKS_TO_MIGRATE,ENABLE_TRACE_FROM_SYNC_CYCLE,ENABLE_TRACE_TO_SYNC_CYCLE,"

# I_MPI_DEBUG=5 KMP_AFFINITY=verbose $MPIEXEC $FLAGS_MPI_BATCH \
# --export=${OLD_EXPORTS}${export_vars} \
# ${NO_NUMA_BALANCING} \
# ./${PROG} ${MXM_PARAMS}


if [ "${RUN_LIKWID}" = "1" ]; then
    module load likwid
    LIKW_EXT="likwid-perfctr -o ${TMP_NAME_RUN}_hwc_R${PMI_RANK}.csv -O -f -c N:0-$((OMP_NUM_THREADS-1)) -g L2CACHE"
fi

# remember current cpuset for process
CUR_CPUSET=$(cut -d':' -f2 <<< $(taskset -c -p $(echo $$)) | xargs)
# echo "${PMI_RANK}: CUR_CPUSET = ${CUR_CPUSET}"

if [ "${RUN_LIKWID}" = "1" ]; then
    echo "Command executed for rank ${PMI_RANK}: ${LIKW_EXT} taskset -c ${CUR_CPUSET} ./${PROG} ${MXM_PARAMS}"
    I_MPI_DEBUG=5 KMP_AFFINITY=verbose $MPIEXEC $FLAGS_MPI_BATCH --export=${OLD_EXPORTS}${export_vars} ${NO_NUMA_BALANCING} ${LIKW_EXT} taskset -c ${CUR_CPUSET} ./${PROG} ${MXM_PARAMS}
else
    echo "Command executed for rank ${PMI_RANK}: ${LIKW_EXT} ./${PROG} ${MXM_PARAMS}"
    I_MPI_DEBUG=5 KMP_AFFINITY=verbose $MPIEXEC $FLAGS_MPI_BATCH --export=${OLD_EXPORTS}${export_vars} ${NO_NUMA_BALANCING} ${LIKW_EXT} ./${PROG} ${MXM_PARAMS}
fi
}

# =============== Settings & environment variables
# N_PROCS=${N_PROCS:-2}
# IS_IMBALANCED=${IS_IMBALANCED:-0}
RUN_LIKWID=${RUN_LIKWID:-1}
# N_REPETITIONS=${N_REPETITIONS:-1}
# CUR_DATE_STR=${CUR_DATE_STR:-"$(date +"%Y%m%d_%H%M%S")"}
# EXE_NAME=${EXE_NAME:-"matrix_app.exe"}

# TASK_GRANULARITY=(300)
# N_THREADS=(8)

# DIR_RESULT="${CUR_DATE_STR}_results/imb${IS_IMBALANCED}_${N_PROCS}procs_${SLURM_NTASKS_PER_NODE}pernode"
# DIR_MXM_EXAMPLE=${DIR_MXM_EXAMPLE:-../../chameleon-apps/applications/matrix_example}
# mkdir -p ${DIR_RESULT}

# export necessary stuff that is used in wrapper script
# export EXE_NAME
# export DIR_MXM_EXAMPLE
# export MXM_PARAMS
# export RUN_LIKWID

# export MIN_REL_LOAD_IMBALANCE_BEFORE_MIGRATION=0.1
# export MAX_TASKS_PER_RANK_TO_MIGRATE_AT_ONCE=1
# export PERCENTAGE_DIFF_TASKS_TO_MIGRATE=0.3
# export MPI_EXEC_CMD="${RUN_SETTINGS_SLURM} ${MPIEXEC} ${FLAGS_MPI_BATCH}"

# for nt in "${N_THREADS[@]}"
# do
#     export OMP_NUM_THREADS=${nt}
#     export MIN_LOCAL_TASKS_IN_QUEUE_BEFORE_MIGRATION=${nt}

#     for g in "${TASK_GRANULARITY[@]}"
#     do
#         echo "Running experiments for granularity ${g} and n_threads=${nt}"
#         export GRANU=${g}
#         for r in {1..${N_REPETITIONS}}
#         do
#             export TMP_NAME_RUN="${DIR_RESULT}/results_${g}_${nt}t_${r}"
#             eval "${MPI_EXEC_CMD} ${MPI_EXPORT_VARS_SLURM} ./wrapper.sh" &> ${TMP_NAME_RUN}.log
#         done
#     done
# done

#########################################################
# ALWAYS_CHECK_PHYSICAL and Map Mode with/out numa bal. #
#########################################################
module unload $CHAMELEON_VERSION
export CHAMELEON_VERSION="chameleon/intel_affinity_debug"
module load $CHAMELEON_VERSION
N_RUNS=1
export AUTOMATIC_NUMA_BALANCING=0
for VAR1 in {0..1}
do  
    export CHAM_AFF_ALWAYS_CHECK_PHYSICAL=${VAR1}
    for VAR2 in 2  # {0..3}
    do
        export CHAM_AFF_MAP_MODE=${VAR2}
        VARIATION_DIR=${LOG_DIR}"/"${VAR1}"_"${VAR2}
        mkdir ${VARIATION_DIR}
        for RUN in {1..${N_RUNS}}
        do
            export TMP_NAME_RUN=${VARIATION_DIR}/R${RUN}
            eval "run_experiment" >>& ${VARIATION_DIR}/R${RUN}.log
            # print some information to check the progression of the job
            squeue -u ka387454 >> ${OUT_DIR}/runtime_progression.log
            echo "Finished "${VAR1}"_"${VAR2}"_R"${RUN} >> ${OUT_DIR}/runtime_progression.log
        done
    done
done



# get the total runtime of the job
squeue -u ka387454