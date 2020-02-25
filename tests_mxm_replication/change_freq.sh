#!/bin/bash


d=$(date -Ins)
echo "$d, rank ${SLURM_PROCID} setting freq $1"
likwid-setFrequencies -f $1
