#!/usr/local_rwth/bin/zsh
#SBATCH --time=00:10:00
#SBATCH --exclusive
#SBATCH --partition=c18m


###############################
# Loading some default values #
###############################
export CHAM_AFF_TASK_SELECTION_STRAT=3
export CHAM_AFF_PAGE_SELECTION_STRAT=8
export CHAM_AFF_PAGE_WEIGHTING_STRAT=2
export CHAM_AFF_CONSIDER_TYPES=1
export CHAM_AFF_PAGE_SELECTION_N=3
export CHAM_AFF_TASK_SELECTION_N=3
export CHAM_AFF_MAP_MODE=0
export CHAM_AFF_ALWAYS_CHECK_PHYSICAL=1
export AUTOMATIC_NUMA_BALANCING=1
export OMP_NUM_THREADS=47
export PROG="mxm_chameleon"
export CHAMELEON_VERSION="chameleon/intel"
export MXM_PARAMS="600 1200 1200 1200 1200"

cd /home/ka387454/repos/chameleon-apps/applications/matrix_example
module use -a /home/ka387454/.modules
module load $CHAMELEON_VERSION

export_vars="CHAMELEON_VERSION,MXM_PARAMS,OMP_NUM_THREADS,CHAM_AFF_TASK_SELECTION_STRAT,CHAM_AFF_PAGE_SELECTION_STRAT,CHAM_AFF_PAGE_WEIGHTING_STRAT,CHAM_AFF_CONSIDER_TYPES,CHAM_AFF_PAGE_SELECTION_N,CHAM_AFF_TASK_SELECTION_N,CHAM_AFF_MAP_MODE,CHAM_AFF_ALWAYS_CHECK_PHYSICAL,NO_NUMA_BALANCING,AUTOMATIC_NUMA_BALANCING,PROG"

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

OMP_PLACES=cores OMP_PROC_BIND=close I_MPI_DEBUG=5 \
KMP_AFFINITY=verbose $MPIEXEC $FLAGS_MPI_BATCH \
--export=PATH,CPLUS_INCLUDE_PATH,C_INCLUDE_PATH,CPATH,INCLUDE,\
LD_LIBRARY_PATH,LIBRARY_PATH,I_MPI_DEBUG,I_MPI_TMI_NBITS_RANK,\
OMP_NUM_THREADS,OMP_PLACES,OMP_PROC_BIND,KMP_AFFINITY,\
MIN_ABS_LOAD_IMBALANCE_BEFORE_MIGRATION,MIN_LOCAL_TASKS_IN_QUEUE_BEFORE_MIGRATION,\
MIN_REL_LOAD_IMBALANCE_BEFORE_MIGRATION,MAX_TASKS_PER_RANK_TO_MIGRATE_AT_ONCE,\
PERCENTAGE_DIFF_TASKS_TO_MIGRATE,ENABLE_TRACE_FROM_SYNC_CYCLE,ENABLE_TRACE_TO_SYNC_CYCLE,\
${export_vars} \
${NO_NUMA_BALANCING} \
./${PROG} ${MXM_PARAMS}
}

#########################################################
#   Test with varying Task selection strategy and mode  #
#########################################################
for VAR1 in 0 1 2 3
do
    export CHAM_AFF_MAP_MODE=${VAR1}
    for VAR2 in {0..8}
    do
    export CHAM_AFF_TASK_SELECTION_STRAT=${VAR2}
    VARIATION_DIR=${OUT_DIR}"/"${VAR1}"_"${VAR2}
    mkdir ${VARIATION_DIR}
        for RUN in {1..20}
        do
            eval "run_experiment" >> ${VARIATION_DIR}/R${RUN}.log
        done
    done
done

##############################
# Chameleon without affinity #
##############################
VARIATION_DIR=${OUT_DIR}"/cham_no_affinity"
for RUN in {1..20}
do
    eval "run_experiment" >> ${VARIATION_DIR}/R${RUN}.log
done

##############################
# Tasking only, no chameleon #
##############################
VARIATION_DIR=${OUT_DIR}"/no_chameleon"
export CHAMELEON_VERSION="chameleon/intel_no_affinity" # Need to load chameleon because of prints in the matrix example
export PROG=mxm_tasking
export OMP_NUM_THREADS=48
for RUN in {1..20}
do
    eval "run_experiment" >> ${VARIATION_DIR}/R${RUN}.log
done