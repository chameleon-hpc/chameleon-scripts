#!/bin/bash

rank=$PMI_RANK

freq_tools=~/samoa/bin/frequency_experiment

#echo "Rank $rank starting rr-wrapper"

freq=$1
t=$2
samoa_cmd="$3"

#echo "Rank $rank, f $freq, t=$t, samoa_cmd $samoa_cmd"

#echo "Rank $rank starting rr daemon"
${freq_tools}/change_freq_rr.sh $freq $t &
pid=$!

#echo "Rank $rank starting samoa"
$samoa_cmd

#echo "Rank $rank finished samoa, resetting frequency settings"
kill $pid
${freq_tools}/frequency_reset.sh 
