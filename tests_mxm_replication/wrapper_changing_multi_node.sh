#!/bin/bash

rank=$PMI_RANK
freq_tools=~/samoa/bin/frequency_experiment

#echo "Hi, this is rank $rank starting the frequency daemon"

#echo "$*"
#echo "$@"

range=$1
t=$2
off=$3
samoa_cmd="$4"

#echo "Range=$range, t=$t, off=$off, samoa_cmd="$samoa_cmd""

${freq_tools}/frequency_changer.sh $range $t $(($off*$rank))&
pid=$!

#echo "Rank $rank is starting samoa"
$samoa_cmd

#echo "Rank $rank has finished samoa and is now resetting its frequency"
kill $pid
${freq_tools}/frequency_reset.sh
