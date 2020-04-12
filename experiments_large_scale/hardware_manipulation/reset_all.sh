#!/usr/local_rwth/bin/zsh
N_NODES=$1
echo "Resetting ${N_NODES} nodes to default"

for i_node in {1..${N_NODES}}
do
    cur_number=$(printf "%03d" ${i_node})
    echo "Resetting lnm${cur_number}"
    #ssh login-hpc2 "ssh lnm${cur_number} -lroot 'zsh /work/jk869269/scripts_experiments_large_scale/reset_node.sh'"
done
