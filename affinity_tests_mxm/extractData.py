#!/usr/bin/python

import os
import re

# name of the new csv file (overwrites existing file)
filename = 'varyTaskstratMapmode.csv'
# name of the directory where the .txt files from the slurm job are
# has to be in the same dir as this .py script
outputs_dir = 'outputs/vary_TaskStrat_MapMode'

find_string = [
    ["CHAM_AFF_TASK_SELECTION_STRAT", "TaskSelectionStrat"],
    ["CHAM_AFF_PAGE_SELECTION_STRAT", "PageSelectionStrat"],
    ["CHAM_AFF_PAGE_WEIGHTING_STRAT", "PageWeightStrat"],
    ["CHAM_AFF_CONSIDER_TYPES", "ConsiderTypes",],
    ["CHAM_AFF_PAGE_SELECTION_N", "PageN"],
    ["CHAM_AFF_TASK_SELECTION_N", "TaskN"],
    ["CHAM_AFF_MAP_MODE", "MapMode"],
    ["CHAM_AFF_ALWAYS_CHECK_PHYSICAL", "CheckPhysical"],
    ["SLURM_JOB_NUM_NODES", "SlurmNodes"],
    ["SLURM_NTASKS_PER_NODE", "SlurmTasksPerNode"],
    ["AUTOMATIC_NUMA_BALANCING", "NumaBalancing"],
    ["MXM_PARAMS", "MatrixSize,MatrixNumTasks,MatrixDistribution"],
    ["Computations with chameleon took", "Time"]
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
                    if param_found[0]=="MXM_PARAMS":
                        # Split up the Matrix parameters
                        start = line.find(find_string[string_idx][0])
                        end = start + len(find_string[string_idx][0])
                        res = line[end:].strip('=\n\r ')
                        res_split = map(int, res.split())
                        matrix_size = res_split[0]
                        matrix_task_dist = res_split[1:]
                        matrix_num_tasks = sum(matrix_task_dist)
                        matrix_task_dist_str = ""
                        for i in range(len(matrix_task_dist)):
                            matrix_task_dist_str += str(matrix_task_dist[i])+" "
                        matrix_task_dist_str = matrix_task_dist_str.rstrip()
                        csv_file.write(str(matrix_size)+","+str(matrix_num_tasks)+","+matrix_task_dist_str)
                        if string_idx < len(find_string)-1:
                            csv_file.write(",")
                        found = True
                        break
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