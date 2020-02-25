#!/bin/bash

export PATH=$PATH:/lrz/sys/tools/likwid/likwid-4.2-phase2/bin

NODES=($LOADL_PROCESSOR_LIST)
NNODES=$LOADL_TOTAL_TASKS

freq_tools=~/samoa/bin/frequency_experiment

rank=$PMI_RANK

#echo "Rank $rank started rr_changer with $1 and $2"

tinit=$(bc<<<"$2*$rank")
sleep $tinit
tnext=$(bc<<<"$2*($NNODES-1)")

while [ 1 ]
do

d=$(date +%s:%6N)
#echo "rank $rank changes frequency to $1 at $d" 
${freq_tools}/change_freq.sh $1
sleep $2
${freq_tools}/frequency_reset.sh
sleep $tnext
done
