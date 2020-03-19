#!/usr/local_rwth/bin/zsh
#SBATCH --time=01:00:00
#SBATCH --exclusive
#SBATCH --account=jara0001
#SBATCH --partition=c16m

# =============== Load desired modules
source ~/.zshrc
source env_ch_intel.sh

# # hack because currently vtune is not supported in batch usage
# module load c_vtune
# export CMD_VTUNE_PREFIX="amplxe-cl –collect hotspots –r ./${CUR_DATE_STR}_profiling_chameleon_${OMP_NUM_THREADS}t -trace-mpi -- "

# =============== Settings & environment variables
IS_DISTRIBUTED=${IS_DISTRIBUTED:-1}
N_PROCS=${N_PROCS:-2}
N_REPETITIONS=${N_REPETITIONS:-3}
CUR_DATE_STR=${CUR_DATE_STR:-"$(date +"%Y%m%d_%H%M%S")"}
RUN_SETTINGS_SLURM=${RUN_SETTINGS_SLURM:-"OMP_PLACES=cores OMP_PROC_BIND=close I_MPI_FABRICS="shm:tmi" I_MPI_DEBUG=5 KMP_AFFINITY=verbose"}
EXPORT_SETTINGS_SLURM=${EXPORT_SETTINGS_SLURM:-"--export=PATH,CPLUS_INCLUDE_PATH,C_INCLUDE_PATH,CPATH,INCLUDE,LD_LIBRARY_PATH,LIBRARY_PATH,I_MPI_DEBUG,I_MPI_TMI_NBITS_RANK,OMP_NUM_THREADS,OMP_PLACES,OMP_PROC_BIND,KMP_AFFINITY,I_MPI_FABRICS,MIN_ABS_LOAD_IMBALANCE_BEFORE_MIGRATION,MIN_LOCAL_TASKS_IN_QUEUE_BEFORE_MIGRATION,MIN_REL_LOAD_IMBALANCE_BEFORE_MIGRATION,MAX_TASKS_PER_RANK_TO_MIGRATE_AT_ONCE,PERCENTAGE_DIFF_TASKS_TO_MIGRATE,ENABLE_TRACE_FROM_SYNC_CYCLE,ENABLE_TRACE_TO_SYNC_CYCLE"}
MPI_EXEC_CMD="${RUN_SETTINGS_SLURM} ${MPIEXEC} "

# === Cholesky Settings
M_SIZES=(15360 23040 30720 46080 61440)
B_SIZES=(128 256 512 1024)
B_CHECK=0
N_THREADS=(23)
SUB_FOLDERS=(pure-parallel)

# === create result directory
if [ "${IS_DISTRIBUTED}" = "1" ]; then
    export SUFFIX_RESULT_DIR="dm"
else
    export SUFFIX_RESULT_DIR="sm"
fi

CUR_DIR=$(pwd)
DIR_RESULT="${CUR_DIR}/${CUR_DATE_STR}_results/${N_PROCS}procs_${SUFFIX_RESULT_DIR}"
DIR_CHOLESKY=${DIR_CHOLESKY:-../../chameleon-apps/applications/cholesky}
mkdir -p ${DIR_RESULT}
cd ${DIR_CHOLESKY}

echo "Setting initial env vars"
export MIN_REL_LOAD_IMBALANCE_BEFORE_MIGRATION=0.1
export MAX_TASKS_PER_RANK_TO_MIGRATE_AT_ONCE=1
export PERCENTAGE_DIFF_TASKS_TO_MIGRATE=0.3

for target in intel chameleon-manual
do
    # load default modules
    module purge
    module load DEVELOP

    # load target specific compiler and libraries
    while IFS='' read -r line || [[ -n "$line" ]]; do
        if  [[ $line == LOAD_COMPILER* ]] || [[ $line == LOAD_LIBS* ]] ; then
        eval "$line"
        fi
    done < "flags_${target}.def"
    module load ${LOAD_COMPILER}
    module load intelmpi/2018
    module load ${LOAD_LIBS}
    module li
  
    for sub in "${SUB_FOLDERS[@]}"
    do
        for version in ch-${target}-par-timing
        do
            for m_size in "${M_SIZES[@]}"
            do
                for b_size in "${B_SIZES[@]}"
                do
                    echo "Running experiments for ${version} and matrix size ${m_size} and block size ${b_size}"
                    for n_thr in "${N_THREADS[@]}"
                    do
                        export OMP_NUM_THREADS=${n_thr}
                        export MIN_LOCAL_TASKS_IN_QUEUE_BEFORE_MIGRATION=${n_thr}
                        for r in {1..${N_REPETITIONS}}
                        do
                            eval "${MPI_EXEC_CMD} ${EXPORT_SETTINGS_SLURM} ${CMD_VTUNE_PREFIX} ${sub}/${version} ${m_size} ${b_size} ${B_CHECK} " &> ${DIR_RESULT}/results_${sub}_${version}_${m_size}_${b_size}_${N_PROCS}procs_${n_thr}t_${r}.log
                        done
                    done
                done
            done
        done
    done
done
