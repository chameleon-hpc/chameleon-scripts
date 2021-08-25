#!/usr/bin/python

import os
import re
import numpy as np
#import statistics as st
import csv

test_name = 'NUM_STEPS_Comparison_4Threads_20210825_112007'
outDir_name = test_name
# test_name = 'ChamStats_'+test_name

# name of the new csv file (overwrites existing file)
filename = test_name + '.csv'
# name of the directory where the .txt files from the slurm job are
# has to be in the same dir as this .py script
outputs_dir = 'outputs/' + outDir_name
logs_dir = outputs_dir + '/logs'

computeTimeStats = False

find_string = [
    # Affinity Settings
    ["CHAM_AFF_TASK_SELECTION_STRAT", "TaskSelectionStrat"],
    ["CHAM_AFF_PAGE_SELECTION_STRAT", "PageSelectionStrat"],
    ["CHAM_AFF_PAGE_WEIGHTING_STRAT", "PageWeightStrat"],
    ["CHAM_AFF_CONSIDER_TYPES", "ConsiderTypes",],
    ["CHAM_AFF_PAGE_SELECTION_N", "PageN"],
    ["CHAM_AFF_TASK_SELECTION_N", "TaskN"],
    ["CHAM_AFF_MAP_MODE", "MapMode"],
    ["CHAM_AFF_ALWAYS_CHECK_PHYSICAL", "CheckPhysical"],
    # SLURM information
    ["SLURM_JOB_NUM_NODES", "SlurmNodes"],
    ["SLURM_NTASKS_PER_NODE", "SlurmTasksPerNode"],
    ["OMP_NUM_THREADS", "OmpNumThreads"],
    # ["AUTOMATIC_NUMA_BALANCING", "NumaBalancing"],
    # ["MXM_PARAMS", "MatrixSize,MatrixNumTasks,MatrixDistribution"],
    ["CHAMELEON_VERSION", "ChameleonVersion"],
    ["CHAM_SETTINGS_STR", "Variation"],
    # ["PROG", "Program"],
    # ["NODELIST","Nodelist"],
    # ["VARIATION_NAME","VariationName"],
    # ["#R0: will create","R0_initTasks"],
    # ["R#0: total effective throughput=","R0_TotalEffectiveThroughput"],
    # ["R#0: task_migration_rate \(tasks/s\)","R0_TaskMigrationRate"],
    # ["R#0: task_processing_rate \(tasks/s\)","R0_TaskProcessingRate"],
    # ["R#0: _num_executed_tasks_overall","R0_NumExecutedTasksOverall"],
    # ["R#0: _num_migration_decision_performed","R0_NumMigrationDecisionsPerformed"],
    # ["R#0: _num_migration_done","R0_NumMigrationsDone"],
    # ["R#0: _num_tasks_offloaded","R0_NumTasksOffloaded"],
    # ["R#0: _time_taskwait_sum sum=","R0_TimeTaskwaitSum"],
    # ["R#0: _time_taskwait_idling_sum sum=","R0_TimeTaskwaitIdlingSum"],
    # ["#R1: will create","R1_initTasks"],
    # ["R#1: task_processing_rate \(tasks/s\)","R1_TaskProcessingRate"],
    # ["R#1: _num_executed_tasks_overall","R1_NumExecutedTasksOverall"],
    # ["R#1: _time_taskwait_sum sum=","R1_TimeTaskwaitSum"],
    # ["R#1: _time_taskwait_idling_sum sum=","R1_TimeTaskwaitIdlingSum"],
    ["Phase time:","PhaseTime"],
    ["GROUP_INDEX","Group"],  # Another Index for Plotting
    ["SOME_INDEX", "SomeIndex"],    # Index for simpler Plotting
    ]

path_to_script = os.path.dirname(os.path.abspath(__file__))
csv_path = path_to_script + "/results/" + filename
csv_file = open(csv_path, 'w')

outputs_path = os.path.join(path_to_script, outputs_dir)
logs_path = os.path.join(path_to_script, logs_dir)

for i in range(len(find_string)):
    csv_file.write(find_string[i][1])
    if i < len(find_string)-1:
        csv_file.write(",")
csv_file.write("\n")

####################################################
############### Function definitions ###############
####################################################    
def getParametersOfFile(cur_log_file_path):
    with open(cur_log_file_path, 'r') as f:
        lines = f.readlines()
        for string_idx in range(len(find_string)):
            # skip part that will be automatically calculated e.g. when calculating time
            if(find_string[string_idx][0] == "-"):
                continue
            found = False
            if(find_string[string_idx][1] == "PhaseTime"): # find the time of the 3rd phase
                PhaseNum = 1
                for line in lines:
                    line = line.replace('\t',' ').rstrip()
                    param_found = re.findall(find_string[string_idx][0], line)
                    if len(param_found) == 0: continue
                    else:
                        if PhaseNum < 3:
                            PhaseNum += 1
                            continue
                        # Get the value of the string 
                        # (the first element after the string without [spaces, new lines, =, tabs])
                        # start = line.find(find_string[string_idx][0])
                        # end = start + len(find_string[string_idx][0])
                        end = re.search(find_string[string_idx][0],line).span()[1]
                        res = line[end:].replace('\t',' ').strip('%=\n\r\t ')
                        res_split = res.split(" ")
                        res_split[0]=res_split[0].replace(",","_")
                        csv_file.write(res_split[0])
                        found = True
                        break
                if not found:
                    csv_file.write("-1")
            else: # find all normal parameters
                for line in lines:
                    line = line.replace('\t',' ').rstrip()
                    param_found = re.findall(find_string[string_idx][0], line)
                    if len(param_found) == 0: continue
                    else:
                        # Get the value of the string 
                        # (the first element after the string without [spaces, new lines, =, tabs])
                        # start = line.find(find_string[string_idx][0])
                        # end = start + len(find_string[string_idx][0])
                        end = re.search(find_string[string_idx][0],line).span()[1]
                        res = line[end:].replace('\t',' ').strip('%=\n\r\t ')
                        res_split = res.split(" ")
                        res_split[0]=res_split[0].replace(",","_")
                        csv_file.write(res_split[0])
                        found = True
                        break
                if not found:
                    csv_file.write("-1")
            csv_file.write(",")

####################################################
####################################################
####################################################

for log_file in os.listdir(logs_path):
    getParametersOfFile(os.path.join(logs_path, log_file))
    # delete last character of line (which is a ",")
    csv_file.seek(-1,os.SEEK_END)
    csv_file.truncate()

    csv_file.write("\n")

csv_file.close()

####################################################
#               Order file                         #
####################################################

rowNames=['Variation','SomeIndex','Group']

path_to_script = os.path.dirname(os.path.abspath(__file__))
file_path = path_to_script+'/results/'+test_name+'.csv'

out_path = path_to_script+'/results/'+test_name+"_ordered.csv"

for rowName in rowNames:
    with open(file_path, 'r') as f_input:
        csv_input = csv.DictReader(f_input)
        data = sorted(csv_input, key=lambda row: row[rowName])

    with open(out_path, 'w') as f_output:    
        csv_output = csv.DictWriter(f_output, fieldnames=csv_input.fieldnames)
        csv_output.writeheader()
        csv_output.writerows(data)

    os.remove(file_path)
    os.rename(out_path, file_path)

