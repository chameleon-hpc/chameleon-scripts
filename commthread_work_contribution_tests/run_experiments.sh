#!/usr/local_rwth/bin/zsh
#SBATCH --time=00:30:00
#SBATCH --exclusive
#SBATCH --account=thes0986
#SBATCH --partition=c18m


#########################################################
#       Loading the hopefully best values               #
#########################################################
# export CHAM_AFF_TASK_SELECTION_STRAT=1      # ALL_LINEAR
# export CHAM_AFF_PAGE_SELECTION_STRAT=2      # EVERY_NTH
# export CHAM_AFF_PAGE_WEIGHTING_STRAT=2      # BY_SIZE
# export CHAM_AFF_CONSIDER_TYPES=1            # ONLY TO
# export CHAM_AFF_PAGE_SELECTION_N=16         # every 16th
# export CHAM_AFF_TASK_SELECTION_N=3          # (not used)
# export CHAM_AFF_MAP_MODE=3                  # COMBINED_MODE
# export CHAM_AFF_ALWAYS_CHECK_PHYSICAL=1     # recheck every time
export AUTOMATIC_NUMA_BALANCING=0           # start with "no_numa_balancing"
export SOME_INDEX=0
export OMP_NUM_THREADS=$((${CPUS_PER_TASK}-1))  # chameleon communication thread
export PROG="mxm_chameleon"
export CHAMELEON_VERSION="chameleon/intel"
export OMP_PLACES=cores 
export OMP_PROC_BIND=spread

export N_RUNS=1

LOG_DIR=${OUT_DIR}"/logs"
mkdir -p ${LOG_DIR}

MY_EXPORTS="CHAMELEON_VERSION,MXM_PARAMS,OMP_NUM_THREADS,CHAM_AFF_TASK_SELECTION_STRAT,CHAM_AFF_PAGE_SELECTION_STRAT,CHAM_AFF_PAGE_WEIGHTING_STRAT,CHAM_AFF_CONSIDER_TYPES,CHAM_AFF_PAGE_SELECTION_N,CHAM_AFF_TASK_SELECTION_N,CHAM_AFF_MAP_MODE,CHAM_AFF_ALWAYS_CHECK_PHYSICAL,NO_NUMA_BALANCING,AUTOMATIC_NUMA_BALANCING,PROG,SOME_INDEX,N_RUNS,DIR_MXM_EXAMPLE,CUR_DIR,CHAM_COMMTHREAD_WORKCONTRIBUTION_LIMIT"

export DIR_MXM_EXAMPLE=${CUR_DIR}/../../chameleon-apps/applications/matrix_example
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

I_MPI_DEBUG=5 KMP_AFFINITY=verbose $MPIEXEC $FLAGS_MPI_BATCH \
--export=PATH,CPLUS_INCLUDE_PATH,C_INCLUDE_PATH,CPATH,INCLUDE,\
LD_LIBRARY_PATH,LIBRARY_PATH,I_MPI_DEBUG,I_MPI_TMI_NBITS_RANK,\
OMP_NUM_THREADS,OMP_PLACES,OMP_PROC_BIND,KMP_AFFINITY,\
MIN_ABS_LOAD_IMBALANCE_BEFORE_MIGRATION,MIN_LOCAL_TASKS_IN_QUEUE_BEFORE_MIGRATION,\
MIN_REL_LOAD_IMBALANCE_BEFORE_MIGRATION,MAX_TASKS_PER_RANK_TO_MIGRATE_AT_ONCE,\
PERCENTAGE_DIFF_TASKS_TO_MIGRATE,ENABLE_TRACE_FROM_SYNC_CYCLE,ENABLE_TRACE_TO_SYNC_CYCLE,\
${MY_EXPORTS} \
${NO_NUMA_BALANCING} \
${DIR_MXM_EXAMPLE}/${PROG} ${MXM_PARAMS}

}

function prep_no_affinity()
{
    export CHAM_AFF_TASK_SELECTION_STRAT=-1
    export CHAM_AFF_PAGE_SELECTION_STRAT=-1
    export CHAM_AFF_PAGE_WEIGHTING_STRAT=-1
    export CHAM_AFF_CONSIDER_TYPES=-1
    export CHAM_AFF_PAGE_SELECTION_N=-1
    export CHAM_AFF_TASK_SELECTION_N=-1
    export CHAM_AFF_MAP_MODE=-1
    export CHAM_AFF_ALWAYS_CHECK_PHYSICAL=-1
    export SOME_INDEX=-1
    module unload $CHAMELEON_VERSION
    export CHAMELEON_VERSION="chameleon/intel_no_affinity"
    module load $CHAMELEON_VERSION
    export PROG="mxm_chameleon"
    export OMP_NUM_THREADS=$((${CPUS_PER_TASK}-1))  # chameleon communication thread
}

function prep_no_chameleon()
{
    export CHAM_AFF_TASK_SELECTION_STRAT=-1
    export CHAM_AFF_PAGE_SELECTION_STRAT=-1
    export CHAM_AFF_PAGE_WEIGHTING_STRAT=-1
    export CHAM_AFF_CONSIDER_TYPES=-1
    export CHAM_AFF_PAGE_SELECTION_N=-1
    export CHAM_AFF_TASK_SELECTION_N=-1
    export CHAM_AFF_MAP_MODE=-1
    export CHAM_AFF_ALWAYS_CHECK_PHYSICAL=-1
    export SOME_INDEX=-1
    module unload $CHAMELEON_VERSION
    export PROG="mxm_tasking"
    export OMP_NUM_THREADS=${CPUS_PER_TASK}
}

#########################################################
#   Task selection strategy and mode                    #
#########################################################
# LOG_DIR=${OUT_DIR}"/../TaskSelStrat_MapMode_"${CUR_DATE_STR}"/logs"
# mkdir -p ${LOG_DIR}

# export SOME_INDEX=-1

# for VAR1 in 0 1 2 3
# do
#     export SOME_INDEX=$(($SOME_INDEX+1))    # for plotting
#     export CHAM_AFF_MAP_MODE=${VAR1}
#     for VAR2 in {0..4}
#     do
#     export CHAM_AFF_TASK_SELECTION_STRAT=${VAR2}
#     VARIATION_DIR=${LOG_DIR}"/"${VAR1}"_"${VAR2}
#     mkdir ${VARIATION_DIR}
#         for RUN in {1..${N_RUNS}}
#         do
#             eval "run_experiment" >>& ${VARIATION_DIR}/R${RUN}.log
#             # print some information to check the progression of the job
#             squeue -u ka387454 >> ${OUT_DIR}/runtime_progression.log
#             echo "Finished"${VAR1}"_"${VAR2}"_R"${RUN} >> ${OUT_DIR}/runtime_progression.log
#         done
#     done
# done

#########################################################
#           Matrix Distribution                         #
#########################################################
module unload $CHAMELEON_VERSION
export CHAMELEON_VERSION="chameleon/intel"
module load $CHAMELEON_VERSION
export PROG="mxm_chameleon"
export SOME_INDEX=0
for VAR1 in -10 0 10 20 50 100
do  
    export SOME_INDEX=$(($SOME_INDEX+1))    # for plotting
    export CHAM_COMMTHREAD_WORKCONTRIBUTION_LIMIT="${VAR1}"
    VARIATION_DIR=${LOG_DIR}"/${SOME_INDEX}_workcontribution_${VAR1}"
    mkdir ${VARIATION_DIR}
    for RUN in {1..${N_RUNS}}
    do
        eval "run_experiment" >>& ${VARIATION_DIR}/R${RUN}.log
        # print some information to check the progression of the job
        squeue -u ka387454 >> ${OUT_DIR}/runtime_progression.log
        echo "Finished "${VAR1}"_R"${RUN} >> ${OUT_DIR}/runtime_progression.log
    done
done

#########################################################
#           Matrix Distribution                         #
#########################################################
# distributions=(
#     "1000 1000 1000 1000"
#     "1500 1000 1000 500"
#     "1500 1500 500 500"
#     "2000 1500 500 0"
#     "3000 1000 0 0"
#     "4000 0 0 0"
# )
# distributions=(
#     "1200 1200"
#     "1500 900"
#     "1800 600"
#     "2100 300"
#     "2400 0"
# )
# export SOME_INDEX=0
# for VAR1 in "${distributions[@]}"
# do  
#     export SOME_INDEX=$(($SOME_INDEX+1))    # for plotting
#     export MXM_DISTRIBUTION="${VAR1}"
#     VARIATION_DIR=${LOG_DIR}"/affinity_"${SOME_INDEX}
#     mkdir ${VARIATION_DIR}
#     for RUN in {1..${N_RUNS}}
#     do
#         eval "run_experiment" >>& ${VARIATION_DIR}/R${RUN}.log
#         # print some information to check the progression of the job
#         squeue -u ka387454 >> ${OUT_DIR}/runtime_progression.log
#         echo "Finished "${VAR1}"_R"${RUN} >> ${OUT_DIR}/runtime_progression.log
#     done
# done
# export SOME_INDEX=0

#########################################################
#           Matrix Distribution No Affinity             #
#########################################################
# prep_no_affinity
# export SOME_INDEX=0
# for VAR1 in "${distributions[@]}"
# do  
#     export SOME_INDEX=$(($SOME_INDEX+1))    # for plotting
#     export MXM_DISTRIBUTION="${VAR1}"
#     VARIATION_DIR=${LOG_DIR}"/no_affinity_"${SOME_INDEX}
#     mkdir ${VARIATION_DIR}
#     for RUN in {1..${N_RUNS}}
#     do
#         eval "run_experiment" >>& ${VARIATION_DIR}/R${RUN}.log
#         # print some information to check the progression of the job
#         squeue -u ka387454 >> ${OUT_DIR}/runtime_progression.log
#         echo "Finished "${VAR1}"_R"${RUN} >> ${OUT_DIR}/runtime_progression.log
#     done
# done
# export SOME_INDEX=0

#########################################################
#           Matrix Distribution No Chameleon            #
#########################################################
# prep_no_chameleon
# export SOME_INDEX=0
# for VAR1 in "${distributions[@]}"
# do  
#     export SOME_INDEX=$(($SOME_INDEX+1))    # for plotting
#     export MXM_DISTRIBUTION="${VAR1}"
#     VARIATION_DIR=${LOG_DIR}"/no_chameleon_"${SOME_INDEX}
#     mkdir ${VARIATION_DIR}
#     for RUN in {1..${N_RUNS}}
#     do
#         eval "run_experiment" >>& ${VARIATION_DIR}/R${RUN}.log
#         # print some information to check the progression of the job
#         squeue -u ka387454 >> ${OUT_DIR}/runtime_progression.log
#         echo "Finished "${VAR1}"_R"${RUN} >> ${OUT_DIR}/runtime_progression.log
#     done
# done
# export SOME_INDEX=0

#########################################################
#*                  Chameleon vanilla                   #
#########################################################
# prep_no_affinity
# VARIATION_DIR=${OUT_DIR}"/logs/cham_no_affinity"
# mkdir ${VARIATION_DIR}
# for RUN in {1..${N_RUNS}}
# do
#     eval "run_experiment" >>& ${VARIATION_DIR}/R${RUN}.log
#     # print some information to check the progression of the job
#     squeue -u ka387454 >> ${OUT_DIR}/runtime_progression.log
#     echo "Finished_no_affinity_R"${RUN} >> ${OUT_DIR}/runtime_progression.log
# done

#########################################################
#*              Tasking only, no chameleon              #
#########################################################
# prep_no_chameleon
# VARIATION_DIR=${OUT_DIR}"/logs/no_chameleon"
# mkdir ${VARIATION_DIR}
# export PROG="mxm_tasking"
# export OMP_NUM_THREADS=${CPUS_PER_TASK}
# for RUN in {1..${N_RUNS}}
# do
#     eval "run_experiment" >>& ${VARIATION_DIR}/R${RUN}.log
#     # print some information to check the progression of the job
#     squeue -u ka387454 >> ${OUT_DIR}/runtime_progression.log
#     echo "Finished_no_chameleon_R"${RUN} >> ${OUT_DIR}/runtime_progression.log
# done

#########################################################
#*          Single independent job for debugging        #
#########################################################
# export CHAM_COMMTHREAD_WORKCONTRIBUTION_LIMIT=1
# export AUTOMATIC_NUMA_BALANCING=0           # start with "no_numa_balancing"
# export OMP_NUM_THREADS=$((${CPUS_PER_TASK}-1))  # chameleon communication thread
# export PROG="mxm_chameleon"
# export CHAMELEON_VERSION="chameleon/intel"
# export OMP_PLACES=cores 
# export OMP_PROC_BIND=spread

# module load $CHAMELEON_VERSION

# VARIATION_DIR=${LOG_DIR}"/with_commthread_workcontribution"
# mkdir ${VARIATION_DIR}

# # export MXM_SIZE=1200

# for RUN in 1
# do
#     eval "run_experiment" >>& ${VARIATION_DIR}/R${RUN}.log
# done

# # copy comparison logs to all executed test directories (copy no chameleon,... to test dirs)
# find "${OUT_DIR}/../" -maxdepth 1 -iname "*${CUR_DATE_STR}" -type d -exec cp -r -n -- ${OUT_DIR}/logs '{}' ';'
# get the total runtime of the job
squeue -u ka387454