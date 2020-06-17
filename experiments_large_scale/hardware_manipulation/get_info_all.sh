#!/usr/local_rwth/bin/zsh
N_NODES=$1
ssh login-hpc2 "zsh /work/jk869269/repos/chameleon/chameleon-scripts/experiments_large_scale/hardware_manipulation/wrapper_get_info_all.sh ${N_NODES}"
