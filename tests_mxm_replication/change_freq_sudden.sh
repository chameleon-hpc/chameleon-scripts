#!/bin/bash


rank=${SLURM_PROCID}

echo "Rank $rank started sudden dist with frequency $1 and t_keep $2 t_next $3"

NODE_LIST=$(scontrol show hostnames ${SLURM_JOB_NODELIST})
NODE_LIST=(${NODE_LIST})

HOST=$(hostname)
#| cut -d"." -f1
HOST=$(echo $HOST | cut -d"." -f1)
#echo $HOST

while [ 1 ]
do

#d=$(date +%s:%6N)
#echo "rank $rank changes frequency to $1 at $d" 
 
if [ "${NODE_LIST[0]}" = "${HOST}" ]
then
./change_freq.sh $1
sleep $2
./frequency_reset.sh
sleep $3
fi

done

