#!/usr/local_rwth/bin/zsh
# Note: 1200000=1.2 GHz
CUR_FREQ=$1
for i in {0..23}
	#echo "${CUR_FREQ}" > /sys/devices/system/cpu/cpu${i}/cpufreq/scaling_min_freq
	echo ${CUR_FREQ} > /sys/devices/system/cpu/cpu${i}/cpufreq/scaling_max_freq
done