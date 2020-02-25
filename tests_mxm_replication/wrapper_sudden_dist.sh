#!/bin/bash

module use -a /lrz/sys/share/modules/extfiles
module load likwid/modified


freq=$1
t=$2
t_next=$3
app_cmd="$4"
app_param="$5"

echo "f $freq, t=$t, app_cmd ${app_cmd}, app_param ${app_param}"

#printenv

#echo "Rank $rank starting rr daemon"
./change_freq_sudden.sh ${freq} $t ${t_next} &
pid=$!

#echo "Rank $rank starting samoa"
${app_cmd} ${app_param}

#echo "Rank $rank finished samoa, resetting frequency settings"
kill $pid
./frequency_reset.sh 
