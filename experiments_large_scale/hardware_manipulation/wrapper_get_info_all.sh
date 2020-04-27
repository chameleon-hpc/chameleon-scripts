#!/usr/local_rwth/bin/zsh
N_NODES=$1
echo "Getting HW info of ${N_NODES} nodes from $(hostname)"

for i_node in {1..${N_NODES}}
do
    cur_number=$(printf "%03d" ${i_node})
    ssh lnm${cur_number} -lroot "zsh /work/jk869269/scripts_experiments_large_scale/node_get_info.sh"
done
