#!/usr/local_rwth/bin/zsh
N_NODES=$1
POWER_CAP=$2
ssh login-hpc2 "zsh /work/jk869269/repos/chameleon/chameleon-scripts/experiments_large_scale/hardware_manipulation/wrapper_set_pc_all.sh ${N_NODES} ${POWER_CAP}"
