#!/bin/bash
#BSUB -J "batch_cholesky"
#BSUB -o batch_cholesky.out.%J
#BSUB -e batch_cholesky.err.%J
#BSUB -W 00:30
##BSUB -m c24m128
#BSUB -m c144m1024
#BSUB -n 1
#BSUB -x
#BSUB -a openmp
#BSUB -P jara0001
##BSUB -M 126000
#BSUB -M 1000000
#BSUB -u j.klinkenberg@itc.rwth-aachen.de
#BSUB -B
#BSUB -N

module use /home/jk869269/.modules
module switch intel intel/18.0
module switch openmpi intelmpi
module load python/3.6.0
module li
python3.6 ./cholesky_compare_versions.py