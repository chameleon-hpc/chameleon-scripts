#!/usr/local_rwth/bin/zsh
N_NODES=$1
POWER_CAP=$2
echo "Setting power cap of ${N_NODES} nodes to ${POWER_CAP} W"

for i_node in {1..${N_NODES}}
do
    cur_number=$(printf "%03d" ${i_node})
    echo "Setting power cap of lnm${cur_number}"
    #ssh login-hpc2 "ssh lnm${cur_number} -lroot 'zsh /work/jk869269/scripts_experiments_large_scale/set_pc.sh ${POWER_CAP}'"
done
