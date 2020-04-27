#!/usr/local_rwth/bin/zsh
N_NODES=$1
CUR_FREQ=$2
ssh login-hpc2 "zsh /work/jk869269/repos/chameleon/chameleon-scripts/experiments_large_scale/hardware_manipulation/wrapper_set_freq_all.sh ${N_NODES} ${CUR_FREQ}"
