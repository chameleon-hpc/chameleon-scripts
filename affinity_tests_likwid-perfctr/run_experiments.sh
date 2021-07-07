#!/usr/local_rwth/bin/zsh
#SBATCH --time=06:00:00
#SBATCH --exclusive
#SBATCH --partition=c18m
#SBATCH --account=thes0986
#SBATCH --hwctr=likwid

CUR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )" # get path of current script

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
# export CHAMELEON_VERSION="chameleon/intel"
export CHAMELEON_VERSION="chameleon/intel_affinity_debug"
export OMP_PLACES=cores 
export OMP_PROC_BIND=close
export DIR_MXM_EXAMPLE=${CUR_DIR}/../../chameleon-apps/applications/matrix_example
export N_RUNS=20

# split PARAMS without having to change the extractData.py script...
export MXM_PARAMS="${MXM_SIZE} ${MXM_DISTRIBUTION}"

if [ "$AUTOMATIC_NUMA_BALANCING" -eq "1" ]
then export NO_NUMA_BALANCING=""
else export NO_NUMA_BALANCING="no_numa_balancing"
fi

source ~/.zshrc
module load ${CHAMELEON_VERSION}

LOG_DIR=${OUT_DIR}"/logs"
mkdir -p ${LOG_DIR}

OLD_EXPORTS="PATH,CPLUS_INCLUDE_PATH,C_INCLUDE_PATH,CPATH,INCLUDE,LD_LIBRARY_PATH,LIBRARY_PATH,I_MPI_DEBUG,I_MPI_TMI_NBITS_RANK,OMP_NUM_THREADS,OMP_PLACES,OMP_PROC_BIND,KMP_AFFINITY,MIN_ABS_LOAD_IMBALANCE_BEFORE_MIGRATION,MIN_LOCAL_TASKS_IN_QUEUE_BEFORE_MIGRATION,MIN_REL_LOAD_IMBALANCE_BEFORE_MIGRATION,MAX_TASKS_PER_RANK_TO_MIGRATE_AT_ONCE,PERCENTAGE_DIFF_TASKS_TO_MIGRATE,ENABLE_TRACE_FROM_SYNC_CYCLE,ENABLE_TRACE_TO_SYNC_CYCLE,"
MY_EXPORTS="CHAMELEON_VERSION,MXM_PARAMS,OMP_NUM_THREADS,CHAM_AFF_TASK_SELECTION_STRAT,CHAM_AFF_PAGE_SELECTION_STRAT,CHAM_AFF_PAGE_WEIGHTING_STRAT,CHAM_AFF_CONSIDER_TYPES,CHAM_AFF_PAGE_SELECTION_N,CHAM_AFF_TASK_SELECTION_N,CHAM_AFF_MAP_MODE,CHAM_AFF_ALWAYS_CHECK_PHYSICAL,NO_NUMA_BALANCING,AUTOMATIC_NUMA_BALANCING,PROG,SOME_INDEX,N_RUNS,RUN_LIKWID,DIR_MXM_EXAMPLE,OUT_DIR,TMP_NAME_RUN"

hostname
module list

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

# printing env needed for extracting data with python script
hostname
module list
env

echo ""
echo "${MPIEXEC} ${FLAGS_MPI_BATCH}"

I_MPI_DEBUG=5 ${MPIEXEC} ${FLAGS_MPI_BATCH} --export=${OLD_EXPORTS}${MY_EXPORTS} ${CUR_DIR}/wrapper.sh

}

#########################################################
# ALWAYS_CHECK_PHYSICAL and Map Mode with/out numa bal. #
#########################################################
# N_RUNS=10
export AUTOMATIC_NUMA_BALANCING=0
# export CHAM_AFF_TASK_SELECTION_STRAT=5 # ALL_LINEAR_FAKE
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
            # exit
        done
    done
done

# get the total runtime of the job
squeue -u ka387454