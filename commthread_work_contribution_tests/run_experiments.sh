#!/usr/local_rwth/bin/zsh
#SBATCH --time=10:00:00
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
# export OMP_NUM_THREADS=$((${CPUS_PER_TASK}-1))  # chameleon communication thread
export OMP_NUM_THREADS=3
export MIN_ABS_LOAD_IMBALANCE_BEFORE_MIGRATION=$((${OMP_NUM_THREADS}*1.3))
export MIN_REL_LOAD_IMBALANCE_BEFORE_MIGRATION=0.1
export PROG="mxm_chameleon"
export CHAMELEON_VERSION="chameleon/intel_comm_contribution"
export OMP_PLACES=cores 
export OMP_PROC_BIND=spread

export N_RUNS=10

LOG_DIR=${OUT_DIR}"/logs"
mkdir -p ${LOG_DIR}

MY_EXPORTS="CHAMELEON_VERSION,MXM_PARAMS,OMP_NUM_THREADS,CHAM_AFF_TASK_SELECTION_STRAT,CHAM_AFF_PAGE_SELECTION_STRAT,CHAM_AFF_PAGE_WEIGHTING_STRAT,CHAM_AFF_CONSIDER_TYPES,CHAM_AFF_PAGE_SELECTION_N,CHAM_AFF_TASK_SELECTION_N,CHAM_AFF_MAP_MODE,CHAM_AFF_ALWAYS_CHECK_PHYSICAL,NO_NUMA_BALANCING,AUTOMATIC_NUMA_BALANCING,PROG,SOME_INDEX,N_RUNS,DIR_MXM_EXAMPLE,CUR_DIR,CHAM_COMMTHREAD_WORKCONTRIBUTION_LIMIT,"

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
    # export SOME_INDEX=-1
    module unload $CHAMELEON_VERSION
    export CHAMELEON_VERSION="chameleon/intel_no_affinity"
    module load $CHAMELEON_VERSION
    export PROG="mxm_chameleon"
    # export OMP_NUM_THREADS=$((${CPUS_PER_TASK}-1))  # chameleon communication thread
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

#*########################################################
#*   Vary Distribution and Work Contribution             #
#*########################################################
distributions=(
    "800 400 200 0"
    "500 400 300 200"
    "350 350 350 350"
)

export GROUP_INDEX=-1

for VAR1 in "${distributions[@]}"
do
    export MXM_DISTRIBUTION="${VAR1}"
    export SOME_INDEX=-1
    export GROUP_INDEX=$(($GROUP_INDEX+1))    # for plotting

    #* Chameleon default
    prep_no_affinity
    export SOME_INDEX=$(($SOME_INDEX+1))    # for plotting
    export CHAM_COMMTHREAD_WORKCONTRIBUTION_LIMIT=0
    VARIATION_DIR=${OUT_DIR}"/logs/Distribution-${GROUP_INDEX}_Cham-Vanilla"
    mkdir ${VARIATION_DIR}
    for RUN in {1..${N_RUNS}}
    do
        eval "run_experiment" >>& ${VARIATION_DIR}/R${RUN}.log
        # print some information to check the progression of the job
        squeue -u ka387454 >> ${OUT_DIR}/runtime_progression.log
        echo "Finished_no_affinity_R"${RUN} >> ${OUT_DIR}/runtime_progression.log
    done

    #* Chameleon with Commthread work contribution
    module unload ${CHAMELEON_VERSION}
    export CHAMELEON_VERSION="chameleon/intel_comm_contribution"
    module load ${CHAMELEON_VERSION}
    for VAR2 in 0 1 10 100 1000 10000 100000 1000000
    do
        export CHAM_COMMTHREAD_WORKCONTRIBUTION_LIMIT=${VAR2}
        export SOME_INDEX=$(($SOME_INDEX+1))    # for plotting
        VARIATION_DIR=${LOG_DIR}"/Distribution-"${GROUP_INDEX}"_Contribution-"${VAR2}
        mkdir ${VARIATION_DIR}
        for RUN in {1..${N_RUNS}}
        do
            eval "run_experiment" >>& ${VARIATION_DIR}/R${RUN}.log
            # print some information to check the progression of the job
            squeue -u ka387454 >> ${OUT_DIR}/runtime_progression.log
            echo "Finished"${GROUP_INDEX}"_"${VAR2}"_R"${RUN} >> ${OUT_DIR}/runtime_progression.log
        done
    done
done

#*########################################################
#*   Vary NumThreads and Work Contribution               #
#*########################################################
# export GROUP_INDEX=-1
# export MXM_DISTRIBUTION="500 400 300 200"

# for VAR1 in 1 2 3 4 5 6 7 8 9 10 11
# do
#     export OMP_NUM_THREADS="${VAR1}"
#     export MIN_ABS_LOAD_IMBALANCE_BEFORE_MIGRATION=$((${OMP_NUM_THREADS}*1.3))
#     export SOME_INDEX=-1
#     export GROUP_INDEX=$(($GROUP_INDEX+1))    # for plotting

#     #* Chameleon default
#     prep_no_affinity
#     export SOME_INDEX=$(($SOME_INDEX+1))    # for plotting
#     export CHAM_COMMTHREAD_WORKCONTRIBUTION_LIMIT=0
#     VARIATION_DIR=${OUT_DIR}"/logs/${VAR1}-Threads_Cham-Vanilla"
#     mkdir ${VARIATION_DIR}
#     for RUN in {1..${N_RUNS}}
#     do
#         eval "run_experiment" >>& ${VARIATION_DIR}/R${RUN}.log
#         # print some information to check the progression of the job
#         squeue -u ka387454 >> ${OUT_DIR}/runtime_progression.log
#         echo "Finished_no_affinity_R"${RUN} >> ${OUT_DIR}/runtime_progression.log
#     done

#     #* Chameleon with Commthread work contribution
#     module unload ${CHAMELEON_VERSION}
#     export CHAMELEON_VERSION="chameleon/intel_comm_contribution"
#     module load ${CHAMELEON_VERSION}
#     for VAR2 in 10000 100000 1000000
#     do
#         export CHAM_COMMTHREAD_WORKCONTRIBUTION_LIMIT=${VAR2}
#         export SOME_INDEX=$(($SOME_INDEX+1))    # for plotting
#         VARIATION_DIR=${LOG_DIR}"/"${VAR1}"-Threads_Contribution-"${VAR2}
#         mkdir ${VARIATION_DIR}
#         for RUN in {1..${N_RUNS}}
#         do
#             eval "run_experiment" >>& ${VARIATION_DIR}/R${RUN}.log
#             # print some information to check the progression of the job
#             squeue -u ka387454 >> ${OUT_DIR}/runtime_progression.log
#             echo "Finished"${GROUP_INDEX}"_"${VAR2}"_R"${RUN} >> ${OUT_DIR}/runtime_progression.log
#         done
#     done
# done

#*########################################################
#*   Vary NumThreads and Task Distributions              #
#*########################################################
# export GROUP_INDEX=-1
# export CHAM_COMMTHREAD_WORKCONTRIBUTION_LIMIT=100000
# distributions=(
#     "800 400 200 0"
#     "500 400 300 200"
#     "350 350 350 350"
# )

# for VAR1 in 1 2 3 4 5 6 7 8 9 10 11
# do
#     export OMP_NUM_THREADS="${VAR1}"
#     export MIN_ABS_LOAD_IMBALANCE_BEFORE_MIGRATION=$((${OMP_NUM_THREADS}*1.3))
#     export SOME_INDEX=-1
#     export GROUP_INDEX=$(($GROUP_INDEX+1))    # for plotting

#     for VAR2 in "${distributions[@]}"
#     do
#         export MXM_DISTRIBUTION="${VAR2}"

#         #* Chameleon default
#         prep_no_affinity
#         export SOME_INDEX=$(($SOME_INDEX+1))    # for plotting
#         VARIATION_DIR=${OUT_DIR}"/logs/${VAR1}-Threads_Distribution-${SOME_INDEX}_Cham-Vanilla"
#         mkdir ${VARIATION_DIR}
#         for RUN in {1..${N_RUNS}}
#         do
#             eval "run_experiment" >>& ${VARIATION_DIR}/R${RUN}.log
#             # print some information to check the progression of the job
#             squeue -u ka387454 >> ${OUT_DIR}/runtime_progression.log
#             echo "Finished_no_contribution_R"${RUN} >> ${OUT_DIR}/runtime_progression.log
#         done

#         #* Chameleon with Commthread work contribution
#         module unload ${CHAMELEON_VERSION}
#         export CHAMELEON_VERSION="chameleon/intel_comm_contribution"
#         module load ${CHAMELEON_VERSION}
#         export SOME_INDEX=$(($SOME_INDEX+1))    # for plotting
#         VARIATION_DIR=${LOG_DIR}"/"${VAR1}"-Threads_Distribution-"${SOME_INDEX}
#         mkdir ${VARIATION_DIR}
#         for RUN in {1..${N_RUNS}}
#         do
#             eval "run_experiment" >>& ${VARIATION_DIR}/R${RUN}.log
#             # print some information to check the progression of the job
#             squeue -u ka387454 >> ${OUT_DIR}/runtime_progression.log
#             echo "Finished"${GROUP_INDEX}"_"${SOME_INDEX}"_R"${RUN} >> ${OUT_DIR}/runtime_progression.log
#         done
#     done
# done

#*########################################################
#*              Vary OpenMP Num Threads                  #
#*########################################################
# export GROUP_INDEX=-1
# export N_RUNS=5
# export MXM_DISTRIBUTION="350 350 350 350"

# for VAR1 in 1 2 3 4 5 6 7 8 9 10 11
# do
#     export SOME_INDEX=-1
#     export GROUP_INDEX=$(($GROUP_INDEX+1))    # for plotting
#     export OMP_NUM_THREADS=${VAR1}
#     export MIN_ABS_LOAD_IMBALANCE_BEFORE_MIGRATION=$((${OMP_NUM_THREADS}*1.3))
#     #* Chameleon default
#     prep_no_affinity
#     export SOME_INDEX=$(($SOME_INDEX+1))    # for plotting
#     export CHAM_COMMTHREAD_WORKCONTRIBUTION_LIMIT=0
#     VARIATION_DIR=${OUT_DIR}"/logs/Threads-${VAR1}_Cham-Vanilla"
#     mkdir ${VARIATION_DIR}
#     for RUN in {1..${N_RUNS}}
#     do
#         eval "run_experiment" >>& ${VARIATION_DIR}/R${RUN}.log
#         # print some information to check the progression of the job
#         squeue -u ka387454 >> ${OUT_DIR}/runtime_progression.log
#         echo "Finished_no_affinity_R"${RUN} >> ${OUT_DIR}/runtime_progression.log
#     done
# done


#########################################################
#*          Single independent job for debugging        #
#########################################################
# export CHAM_COMMTHREAD_WORKCONTRIBUTION_LIMIT=1
# export AUTOMATIC_NUMA_BALANCING=0           # start with "no_numa_balancing"
# export OMP_NUM_THREADS=$((${CPUS_PER_TASK}-1))  # chameleon communication thread
# export MIN_ABS_LOAD_IMBALANCE_BEFORE_MIGRATION=$((${OMP_NUM_THREADS}*1.3))
# export PROG="mxm_chameleon"
# export CHAMELEON_VERSION="chameleon/intel_comm_contribution"
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