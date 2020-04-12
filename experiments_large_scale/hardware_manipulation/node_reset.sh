#!/usr/local_rwth/bin/zsh

echo "Resetting $(hostname)"
# the system default TIME_WINDOW is 1
# but I set the TIME_WINDOW to a value lower than 0.01 to obain effective power capping
/w0/tmp/power_gov -r TIME_WINDOW -s 0.01 -d PKG
# 105 is the TDP
/w0/tmp/power_gov -r POWER_LIMIT -s 105 -d PKG

for i in {0..23}
	cat  /sys/devices/system/cpu/cpu${i}/cpufreq/cpuinfo_max_freq > /sys/devices/system/cpu/cpu${i}/cpufreq/scaling_max_freq 
	cat  /sys/devices/system/cpu/cpu${i}/cpufreq/cpuinfo_min_freq > /sys/devices/system/cpu/cpu${i}/cpufreq/scaling_min_freq 
done