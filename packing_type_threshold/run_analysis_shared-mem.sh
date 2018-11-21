#!/bin/bash
#BSUB -J "batch_analyse_threshold_packing_type_sm"
#BSUB -o batch_analyse_threshold_packing_type_sm.out.%J
#BSUB -e batch_analyse_threshold_packing_type_sm.err.%J
#BSUB -W 09:00
##BSUB -m c24m128
#BSUB -m c144m1024
#BSUB -n 2
#BSUB -x
#BSUB -a intelmpi
#BSUB -P jara0001
##BSUB -M 126000
#BSUB -M 1000000
#BSUB -u j.klinkenberg@itc.rwth-aachen.de
#BSUB -B
#BSUB -N

module use /home/jk869269/.modules
source /home/jk869269/util/includes/env_chameleon_dev.sh

# workaround because clang offloading and Intel MPI are messing around with TMI in OPA fabric somehow
export I_MPI_FABRICS="shm:dapl"

module unload chameleon-lib
module load chameleon-lib/1.0
module li
python3.6 ./analyze_threshold_packing_type.py "shared_buffer" 13

module unload chameleon-lib
module load chameleon-lib/1.0-zero-copy
module li
python3.6 ./analyze_threshold_packing_type.py "shared_zero-copy" 13
