#!/usr/bin/python

import os
import re

# name of the new csv file (overwrites existing file)
filename = 'results/preTesting.csv'
# name of the directory where the .txt files from the slurm job are
# has to be in the same dir as this .py script
outputs_dir = 'outputs/preTesting'

find_string = [
    ["CHAM_AFF_TASK_SELECTION_STRAT", "task sel. strat"],
    ["CHAM_AFF_PAGE_SELECTION_STRAT", "page sel. strat."],
    ["CHAM_AFF_PAGE_WEIGHTING_STRAT", "page weight. strat."],
    ["CHAM_AFF_CONSIDER_TYPES", "consider types",],
    ["CHAM_AFF_PAGE_SELECTION_N", "page n"],
    ["CHAM_AFF_TASK_SELECTION_N", "task n"],
    ["CHAM_AFF_MAP_MODE", "map mode"],
    ["CHAM_AFF_ALWAYS_CHECK_PHYSICAL", "always check physical"],
    ["SLURM_JOB_NUM_NODES", "slurm nodes"],
    ["SLURM_NTASKS_PER_NODE", "slurm tasks p. node"],
    ["Computations with chameleon took", "time"]
    ]

path_to_script = os.path.dirname(os.path.abspath(__file__))
csv_file = open(os.path.join(path_to_script, filename), 'w')

outputs_path = os.path.join(path_to_script, outputs_dir)

for i in range(len(find_string)):
    csv_file.write(find_string[i][1])
    if i < len(find_string)-1:
        csv_file.write(",")
csv_file.write("\n")

for read_file in os.listdir(outputs_path):
    with open(os.path.join(outputs_path, read_file), 'r') as f:
        lines = f.readlines()
        for string_idx in range(len(find_string)):
            found = False
            for line in lines:
                line = line.rstrip()
                param_found = re.findall(find_string[string_idx][0], line)
                if len(param_found) == 0: continue
                else:
                    # Get the value of the string 
                    # (everything after the string without [spaces, new lines, =])
                    start = line.find(find_string[string_idx][0])
                    end = start + len(find_string[string_idx][0])
                    res = line[end:].strip('=\n\r ')
                    csv_file.write(res)
                    if string_idx < len(find_string)-1:
                        csv_file.write(",")
                    found = True
                    break
            if not found:
                # Parameter not in the file
                csv_file.write("-1,")
    csv_file.write("\n")

csv_file.close()