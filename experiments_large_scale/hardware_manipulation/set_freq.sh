#!/usr/local_rwth/bin/zsh
# Sets a frequency for a specific node
CUR_NODE=$1
CUR_FREQ=$2
ssh login-hpc2 "ssh ${CUR_NODE} -lroot 'zsh /work/jk869269/scripts_experiments_large_scale/node_set_freq.sh ${CUR_FREQ}'"
