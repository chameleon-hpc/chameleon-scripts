#!/bin/bash

export PATH=$PATH:/lrz/sys/tools/likwid/likwid-4.2-phase2/bin

FREQS=(2.600 2.5 2.4 2.3 2.2 2.1 2.0 1.9 1.8 1.7 1.6 1.5 1.4 1.3 1.2)
#PATTERN=(11 2 4 12 7 13 5 10 0 6 3 14 1 8 9)

while [ 1 ] 
do
 for i in `seq 0 $1`;
 do
   #ind=${PATTERN[$i]}
  # echo $ind
  # echo ${FREQ[$ind]}
   ~/samoa/bin/frequency_experiment/change_freq.sh ${FREQS[$((($i+$3)%($1+1)))]}
#likwid-setFrequencies -p
  # h=$(hostname)
  # echo "$h setting to ${FREQS[$((($i+$3)%($1+1)))]}"
   sleep $2
 done
done

