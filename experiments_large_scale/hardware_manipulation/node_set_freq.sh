#!/usr/local_rwth/bin/zsh
# Note: 1200000=1.2 GHz
CUR_FREQ=$1
echo "Setting CPU frequency of $(hostname) to ${CUR_FREQ}"
for i in {0..23}
do
	#echo "${CUR_FREQ}" > /sys/devices/system/cpu/cpu${i}/cpufreq/scaling_min_freq
	echo ${CUR_FREQ} > /sys/devices/system/cpu/cpu${i}/cpufreq/scaling_max_freq
done
