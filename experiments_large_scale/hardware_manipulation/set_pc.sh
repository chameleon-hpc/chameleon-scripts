#!/usr/local_rwth/bin/zsh
POWER_CAP=$1
/w0/tmp/power_gov -r TIME_WINDOW -s 0.01 -d PKG
/w0/tmp/power_gov -r POWER_LIMIT -s  ${POWER_CAP} -d PKG