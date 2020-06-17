#!/usr/local_rwth/bin/zsh

export CUR_DATE_STR="$(date +"%Y%m%d_%H%M%S")"
CUR_DIR=$(pwd)
DIR_CHOLESKY=${DIR_CHOLESKY:-../../chameleon-apps/applications/cholesky}
SUB_FOLDERS=(pure-parallel singlecom-deps)

# Build versions
cd ${DIR_CHOLESKY}
for target in ompss intel chameleon-intel
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
        # make corresponding targets
        TARGET=${target} make -C ${sub} clean all -j8
    done
done

cd ${CUR_DIR}

: << COMMENT
# 2 node job - shared memory
export IS_DISTRIBUTED=0
export N_PROCS=2
sbatch --nodes=1 --ntasks-per-node=2 --cpus-per-task=12 --job-name=cham_cholesky_tests_2n_sm --output=cham_cholesky_tests_2n_sm.%J.txt --export=IS_DISTRIBUTED,CUR_DATE_STR,N_PROCS,N_THREADS run_experiments.sh
COMMENT

# 2 node job - distributed memory
export IS_DISTRIBUTED=1
export N_PROCS=2
sbatch --nodes=2 --ntasks-per-node=1 --cpus-per-task=24 --job-name=cham_cholesky_tests_2n_dm --output=cham_cholesky_tests_2n_dm.%J.txt --export=IS_DISTRIBUTED,CUR_DATE_STR,N_PROCS,N_THREADS run_experiments.sh

: << COMMENT
# 4 node job - shared memory
export IS_DISTRIBUTED=0
export N_PROCS=4
sbatch --nodes=1 --ntasks-per-node=4 --cpus-per-task=6 --job-name=cham_cholesky_tests_4n_sm --output=cham_cholesky_tests_4n_sm.%J.txt --export=IS_DISTRIBUTED,CUR_DATE_STR,N_PROCS,N_THREADS run_experiments.sh

# 4 node job - distributed memory
export IS_DISTRIBUTED=1
export N_PROCS=4
sbatch --nodes=4 --ntasks-per-node=1 --cpus-per-task=24 --job-name=cham_cholesky_tests_4n_dm --output=cham_cholesky_tests_4n_dm.%J.txt --export=IS_DISTRIBUTED,CUR_DATE_STR,N_PROCS,N_THREADS run_experiments.sh

# 8 node job - distributed memory
export IS_DISTRIBUTED=1
export N_PROCS=8
sbatch --nodes=8 --ntasks-per-node=1 --cpus-per-task=24 --job-name=cham_cholesky_tests_8n_dm --output=cham_cholesky_tests_8n_dm.%J.txt --export=IS_DISTRIBUTED,CUR_DATE_STR,N_PROCS,N_THREADS run_experiments.sh
COMMENT
