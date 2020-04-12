#!/usr/local_rwth/bin/zsh
N_NODES=$1
CUR_FREQ=$2
echo "Setting CPU freq of ${N_NODES} nodes to ${CUR_FREQ}"

for i_node in {1..${N_NODES}}
do
    cur_number=$(printf "%03d" ${i_node})
    ssh login-hpc2 "ssh lnm${cur_number} -lroot 'zsh /work/jk869269/scripts_experiments_large_scale/node_set_freq.sh ${CUR_FREQ}'"
done
