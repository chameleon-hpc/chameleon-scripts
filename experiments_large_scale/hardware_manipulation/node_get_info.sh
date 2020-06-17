#!/usr/local_rwth/bin/zsh

echo "HW info for $(hostname)"

/w0/tmp/power_gov -i | grep "RAPL_POWER_LIMIT:"

echo "Min Freq: $(cat /sys/devices/system/cpu/cpu23/cpufreq/scaling_min_freq)"
echo "Max Freq: $(cat /sys/devices/system/cpu/cpu23/cpufreq/scaling_max_freq)"
echo "Cur Freq: $(cat /sys/devices/system/cpu/cpu23/cpufreq/cpuinfo_cur_freq)"

