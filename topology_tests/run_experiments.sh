#!/usr/local_rwth/bin/zsh
#SBATCH --time=01:00:00
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
export MIGRATION_OFFLOAD_TO_SINGLE_RANK=1
export TOPO_ORDERED_LIST_SELECT=0
# others
export AUTOMATIC_NUMA_BALANCING=0           # start with "no_numa_balancing"
export SOME_INDEX=0
# export GROUP_INDEX=0
export OMP_NUM_THREADS=$((${CPUS_PER_TASK}-1))  # chameleon communication thread
export PROG="mxm_chameleon"
export CHAMELEON_VERSION="chameleon/intel_tool"
export OMP_PLACES=cores 
export OMP_PROC_BIND=close

export N_RUNS=5

LOG_DIR=${OUT_DIR}"/logs"
mkdir -p ${LOG_DIR}

OLD_EXPORTS="PATH,CPLUS_INCLUDE_PATH,C_INCLUDE_PATH,CPATH,INCLUDE,LD_LIBRARY_PATH,LIBRARY_PATH,I_MPI_DEBUG,I_MPI_TMI_NBITS_RANK,OMP_NUM_THREADS,OMP_PLACES,OMP_PROC_BIND,KMP_AFFINITY,MIN_ABS_LOAD_IMBALANCE_BEFORE_MIGRATION,MIN_LOCAL_TASKS_IN_QUEUE_BEFORE_MIGRATION,MIN_REL_LOAD_IMBALANCE_BEFORE_MIGRATION,MAX_TASKS_PER_RANK_TO_MIGRATE_AT_ONCE,PERCENTAGE_DIFF_TASKS_TO_MIGRATE,ENABLE_TRACE_FROM_SYNC_CYCLE,ENABLE_TRACE_TO_SYNC_CYCLE,"
MY_EXPORTS="CHAMELEON_VERSION,MXM_PARAMS,PROCS_PER_NODE,OMP_NUM_THREADS,CHAM_AFF_TASK_SELECTION_STRAT,CHAM_AFF_PAGE_SELECTION_STRAT,CHAM_AFF_PAGE_WEIGHTING_STRAT,CHAM_AFF_CONSIDER_TYPES,CHAM_AFF_PAGE_SELECTION_N,CHAM_AFF_TASK_SELECTION_N,CHAM_AFF_MAP_MODE,CHAM_AFF_ALWAYS_CHECK_PHYSICAL,NO_NUMA_BALANCING,AUTOMATIC_NUMA_BALANCING,PROG,SOME_INDEX,N_RUNS,DIR_APPLICATION,CUR_DIR,CHAMELEON_TOOL_LIBRARIES,TOPO_MIGRATION_STRAT,MIGRATION_OFFLOAD_TO_SINGLE_RANK,GROUP_INDEX,TOPO_ORDERED_LIST_SELECT,NODELIST,VARIATION_NAME"

# export DIR_APPLICATION=${CUR_DIR}/../../chameleon-apps/applications/matrix_example
# cd /home/ka387454/repos/chameleon-apps/applications/matrix_example
source ~/.zshrc
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

#########################################################
#                   Testing                             #
#########################################################
# SOME_INDEX identifies bars in one GROUP_INDEX
# GROUP_INDEX identifies different GROUP_INDEXs of bars (e.g. 4PPN_S600_OLS0_O1)
# 4PPN := 4 Procs Per Node
# S600 := Matrix Size 600
# OLS0 := Ordered List Select = 0
# OS1 := "Only 1" Offload to only a single rank

function setMatrixDistribution(){
if [ "$PROCS_PER_NODE" -eq "4" ] && [ "$MXM_SIZE" -eq "600" ]
then 
export MXM_DISTRIBUTION=\
"1500 1000 500 0 "\
"1500 1000 500 0 "\
"1500 1000 500 0 "\
"1500 1000 500 0 "\
"1500 1000 500 0 "\
"1500 1000 500 0"
fi
if [ "$PROCS_PER_NODE" -eq "2" ] && [ "$MXM_SIZE" -eq "600" ]
then 
export MXM_DISTRIBUTION=\
"1500 0 "\
"1500 0 "\
"1500 0 "\
"1500 0 "\
"1500 0 "\
"1500 0"
fi
if [ "$PROCS_PER_NODE" -eq "4" ] && [ "$MXM_SIZE" -eq "90" ]
then 
export MXM_DISTRIBUTION=\
"20000 10000 5000 0 "\
"20000 10000 5000 0 "\
"20000 10000 5000 0 "\
"20000 10000 5000 0 "\
"20000 10000 5000 0 "\
"20000 10000 5000 0"
fi
if [ "$PROCS_PER_NODE" -eq "2" ] && [ "$MXM_SIZE" -eq "90" ]
then 
export MXM_DISTRIBUTION=\
"20000 0 "\
"20000 0 "\
"20000 0 "\
"20000 0 "\
"20000 0 "\
"20000 0"
fi
}

for var_size in 90 600
do
export MXM_SIZE=${var_size}
setMatrixDistribution
echo ${MXM_DISTRIBUTION}

for var_ols in 0 1
do
export TOPO_ORDERED_LIST_SELECT=${var_ols}

for var_offload_single in 0 1
do
# ordered list select only offloads to max 1 rank, hence offload single is unnecessary
if [ "$var_ols" -eq "1" ] && [ "$var_offload_single" -eq "1" ]
then break
fi
export MIGRATION_OFFLOAD_TO_SINGLE_RANK=${var_offload_single}

export GROUP_INDEX=$(($GROUP_INDEX+1))    # for plotting
export SOME_INDEX=-1

################ Topology Optimized #####################
module unload ${CHAMELEON_VERSION}
export CHAMELEON_VERSION="chameleon/intel_tool"
module load ${CHAMELEON_VERSION}
export TOPO_MIGRATION_STRAT=1 # topology aware nearest

export SOME_INDEX=$(($SOME_INDEX+1))    # for plotting
export VARIATION_NAME="${PROCS_PER_NODE}PPN_S${MXM_SIZE}_OLS${TOPO_ORDERED_LIST_SELECT}_OS${MIGRATION_OFFLOAD_TO_SINGLE_RANK}_TopologyNearest"
VARIATION_DIR=${LOG_DIR}"/${VARIATION_NAME}"
mkdir ${VARIATION_DIR}
for RUN in {1..${N_RUNS}}
do
    eval "run_experiment" >>& ${VARIATION_DIR}/R${RUN}.log
    # print some information to check the progression of the job
    squeue -u ka387454 >> ${OUT_DIR}/runtime_progression.log
    echo "Finished_TopologyNearest_R"${RUN} >> ${OUT_DIR}/runtime_progression.log
done

################ Topology Worst Case ###################
module unload ${CHAMELEON_VERSION}
export CHAMELEON_VERSION="chameleon/intel_tool"
module load ${CHAMELEON_VERSION}
export TOPO_MIGRATION_STRAT=2 # topology aware most distant

export SOME_INDEX=$(($SOME_INDEX+1))    # for plotting
export VARIATION_NAME="${PROCS_PER_NODE}PPN_S${MXM_SIZE}_OLS${TOPO_ORDERED_LIST_SELECT}_OS${MIGRATION_OFFLOAD_TO_SINGLE_RANK}_TopologyDistant"
VARIATION_DIR=${LOG_DIR}"/${VARIATION_NAME}"
mkdir ${VARIATION_DIR}
for RUN in {1..${N_RUNS}}
do
    eval "run_experiment" >>& ${VARIATION_DIR}/R${RUN}.log
    # print some information to check the progression of the job
    squeue -u ka387454 >> ${OUT_DIR}/runtime_progression.log
    echo "Finished_TopologyDistant_R"${RUN} >> ${OUT_DIR}/runtime_progression.log
done

################ topology aware migration with priority [over 1 switch > over 3 switches > same node] ################
module unload ${CHAMELEON_VERSION}
export CHAMELEON_VERSION="chameleon/intel_tool"
module load ${CHAMELEON_VERSION}
export TOPO_MIGRATION_STRAT=3

export SOME_INDEX=$(($SOME_INDEX+1))    # for plotting
export VARIATION_NAME="${PROCS_PER_NODE}PPN_S${MXM_SIZE}_OLS${TOPO_ORDERED_LIST_SELECT}_OS${MIGRATION_OFFLOAD_TO_SINGLE_RANK}_Topology2Hops"
VARIATION_DIR=${LOG_DIR}"/${VARIATION_NAME}"
mkdir ${VARIATION_DIR}
for RUN in {1..${N_RUNS}}
do
    eval "run_experiment" >>& ${VARIATION_DIR}/R${RUN}.log
    # print some information to check the progression of the job
    squeue -u ka387454 >> ${OUT_DIR}/runtime_progression.log
    echo "Finished_Topology2Hops_R"${RUN} >> ${OUT_DIR}/runtime_progression.log
done


done # offload single loop
done # OLS loop

########### Chameleon not topology aware ###############
module unload ${CHAMELEON_VERSION}
export CHAMELEON_VERSION="chameleon/intel"
module load ${CHAMELEON_VERSION}
export TOPO_MIGRATION_STRAT=0

export SOME_INDEX=$(($SOME_INDEX+1))    # for plotting
export VARIATION_NAME="${PROCS_PER_NODE}PPN_S${MXM_SIZE}_ChameleonNoTopo"
VARIATION_DIR=${LOG_DIR}"/${VARIATION_NAME}"
mkdir ${VARIATION_DIR}
for RUN in {1..${N_RUNS}}
do
    eval "run_experiment" >>& ${VARIATION_DIR}/R${RUN}.log
    # print some information to check the progression of the job
    squeue -u ka387454 >> ${OUT_DIR}/runtime_progression.log
    echo "Finished_ChameleonNoTopo_R"${RUN} >> ${OUT_DIR}/runtime_progression.log
done

############ No Migration at all ########################
# module unload ${CHAMELEON_VERSION}
# export CHAMELEON_VERSION="chameleon/intel_aff_no_commthread"
# module load ${CHAMELEON_VERSION}
# export TOPO_MIGRATION_STRAT=-1 # topology aware most distant

# export SOME_INDEX=$(($SOME_INDEX+1))    # for plotting
# export VARIATION_NAME="${PROCS_PER_NODE}PPN_S${MXM_SIZE}_NoCommThread"
# VARIATION_DIR=${LOG_DIR}"/${VARIATION_NAME}"
# mkdir ${VARIATION_DIR}
# for RUN in {1..${N_RUNS}}
# do
#     eval "run_experiment" >>& ${VARIATION_DIR}/R${RUN}.log
#     # print some information to check the progression of the job
#     squeue -u ka387454 >> ${OUT_DIR}/runtime_progression.log
#     echo "Finished_NoCommThread_R"${RUN} >> ${OUT_DIR}/runtime_progression.log
# done

done # MxM Size loop

# copy comparison logs to all executed test directories (copy no chameleon,... to test dirs)
# find "${OUT_DIR}/../" -maxdepth 1 -iname "*${CUR_DATE_STR}" -type d -exec cp -r -n -- ${OUT_DIR}/logs '{}' ';'
# get the total runtime of the job
squeue -u ka387454