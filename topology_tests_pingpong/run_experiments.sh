#!/usr/local_rwth/bin/zsh
#SBATCH --time=02:00:00
#SBATCH --exclusive
#SBATCH --account=thes0986
##SBATCH --partition=c18m


#########################################################
#       Loading the hopefully best values               #
#########################################################
# affinity
export CHAM_AFF_TASK_SELECTION_STRAT=1      # ALL_LINEAR
export CHAM_AFF_PAGE_SELECTION_STRAT=2      # EVERY_NTH
export CHAM_AFF_PAGE_WEIGHTING_STRAT=2      # BY_SIZE
export CHAM_AFF_CONSIDER_TYPES=1            # ONLY TO
export CHAM_AFF_PAGE_SELECTION_N=16         # every 16th
export CHAM_AFF_TASK_SELECTION_N=3          # (not used)
export CHAM_AFF_MAP_MODE=3                  # COMBINED_MODE
export CHAM_AFF_ALWAYS_CHECK_PHYSICAL=1     # recheck every time
# topology
export TOPO_MIGRATION_STRAT=1
# others
export AUTOMATIC_NUMA_BALANCING=0           # start with "no_numa_balancing"
export SOME_INDEX=0
export OMP_NUM_THREADS=$((${CPUS_PER_TASK}-1))  # chameleon communication thread
export PROG="pingpong.exe"
export CHAMELEON_VERSION="chameleon/intel_tool"
export OMP_PLACES=cores 
export OMP_PROC_BIND=close

export N_RUNS=10

LOG_DIR=${OUT_DIR}"/logs"
mkdir -p ${LOG_DIR}

OLD_EXPORTS="PATH,CPLUS_INCLUDE_PATH,C_INCLUDE_PATH,CPATH,INCLUDE,LD_LIBRARY_PATH,LIBRARY_PATH,I_MPI_DEBUG,I_MPI_TMI_NBITS_RANK,OMP_NUM_THREADS,OMP_PLACES,OMP_PROC_BIND,KMP_AFFINITY,MIN_ABS_LOAD_IMBALANCE_BEFORE_MIGRATION,MIN_LOCAL_TASKS_IN_QUEUE_BEFORE_MIGRATION,MIN_REL_LOAD_IMBALANCE_BEFORE_MIGRATION,MAX_TASKS_PER_RANK_TO_MIGRATE_AT_ONCE,PERCENTAGE_DIFF_TASKS_TO_MIGRATE,ENABLE_TRACE_FROM_SYNC_CYCLE,ENABLE_TRACE_TO_SYNC_CYCLE,"
MY_EXPORTS="CHAMELEON_VERSION,MXM_PARAMS,OMP_NUM_THREADS,CHAM_AFF_TASK_SELECTION_STRAT,CHAM_AFF_PAGE_SELECTION_STRAT,CHAM_AFF_PAGE_WEIGHTING_STRAT,CHAM_AFF_CONSIDER_TYPES,CHAM_AFF_PAGE_SELECTION_N,CHAM_AFF_TASK_SELECTION_N,CHAM_AFF_MAP_MODE,CHAM_AFF_ALWAYS_CHECK_PHYSICAL,NO_NUMA_BALANCING,AUTOMATIC_NUMA_BALANCING,PROG,SOME_INDEX,N_RUNS,DIR_APPLICATION,CUR_DIR,CHAMELEON_TOOL_LIBRARIES,TOPO_MIGRATION_STRAT"

# export DIR_APPLICATION=${CUR_DIR}/../../chameleon-apps/applications/matrix_example
# cd /home/ka387454/repos/chameleon-apps/applications/matrix_example
source ~/.zshrc
module load $CHAMELEON_VERSION

#########################################################
#                   Functions                           #
#########################################################

function run_experiment()
{

if [ "$AUTOMATIC_NUMA_BALANCING" -eq "1" ]
then NO_NUMA_BALANCING=""
else NO_NUMA_BALANCING="no_numa_balancing"
fi

hostname
module list
env

echo ""
echo "${MPIEXEC} ${FLAGS_MPI_BATCH}"

# I_MPI_DEBUG=5 KMP_AFFINITY=verbose $MPIEXEC $FLAGS_MPI_BATCH \
# --export=PATH,CPLUS_INCLUDE_PATH,C_INCLUDE_PATH,CPATH,INCLUDE,\
# LD_LIBRARY_PATH,LIBRARY_PATH,I_MPI_DEBUG,I_MPI_TMI_NBITS_RANK,\
# OMP_NUM_THREADS,OMP_PLACES,OMP_PROC_BIND,KMP_AFFINITY,\
# MIN_ABS_LOAD_IMBALANCE_BEFORE_MIGRATION,MIN_LOCAL_TASKS_IN_QUEUE_BEFORE_MIGRATION,\
# MIN_REL_LOAD_IMBALANCE_BEFORE_MIGRATION,MAX_TASKS_PER_RANK_TO_MIGRATE_AT_ONCE,\
# PERCENTAGE_DIFF_TASKS_TO_MIGRATE,ENABLE_TRACE_FROM_SYNC_CYCLE,ENABLE_TRACE_TO_SYNC_CYCLE,\
# ${MY_EXPORTS} \
# ${NO_NUMA_BALANCING} \
# ${DIR_APPLICATION}/${PROG} ${MXM_PARAMS}

I_MPI_DEBUG=5 ${MPIEXEC} ${FLAGS_MPI_BATCH} --export=${OLD_EXPORTS}${MY_EXPORTS} ${CUR_DIR}/wrapper.sh

}

# LOG_DIR=${OUT_DIR}"/../TaskSelStrat_MapMode_"${CUR_DATE_STR}"/logs"
# mkdir -p ${LOG_DIR}

export SOME_INDEX=${REGION}
VARIATION_DIR=${LOG_DIR}"/Region_"${REGION}
mkdir ${VARIATION_DIR}
for RUN in {1..${N_RUNS}}
do
    eval "run_experiment" >>& ${VARIATION_DIR}/R${RUN}.log
    # print some information to check the progression of the job
    squeue -u ka387454 >> ${OUT_DIR}/runtime_progression.log
    echo "Finished Region_"${REGION}"_R"${RUN} >> ${OUT_DIR}/runtime_progression.log
done

# copy comparison logs to all executed test directories (copy no chameleon,... to test dirs)
find "${OUT_DIR}/../" -maxdepth 1 -iname "*${CUR_DATE_STR}" -type d -exec cp -r -n -- ${OUT_DIR}/logs '{}' ';'
# get the total runtime of the job
squeue -u ka387454