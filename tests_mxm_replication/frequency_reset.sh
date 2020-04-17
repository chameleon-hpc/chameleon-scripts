#!/bin/bash

module use -a /lrz/sys/share/modules/extfiles
module load likwid/modified

d=$(date -Ins)
echo "$d, rank ${SLURM_PROCID} resetting freq "  
likwid-setFrequencies -f 2.300
