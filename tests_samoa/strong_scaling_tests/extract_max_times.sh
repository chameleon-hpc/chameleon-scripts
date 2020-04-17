#!/bin/bash

input_base="20191004_152043_results"
input_stealing="20191002_133432_results"
input_tool="20191022_121607_results"

extract_tool="/home/ps659535/chameleon/chameleon-scripts/phase_analysis/extract_max_taskwait.py"

procs=( 1 2 4 8 16 32 )

for p in ${procs[@]}
do
# python $extract_tool  ${input_base}/${p}procs_base_chameleon/results_no_stealing_t24_r1_chameleon_strong.log $p ${p}_procs_taskwait_base
# python $extract_tool  ${input_stealing}/${p}procs_rep_0/results_stealing_t23_r1_chameleon_strong.log $p ${p}_procs_taskwait_stealing
  python $extract_tool  ${input_tool}/${p}procs_rep_3/results_stealing_t23_r1_chameleon_tool_strong.log $p ${p}_procs_taskwait_stealing_tool
done
done

