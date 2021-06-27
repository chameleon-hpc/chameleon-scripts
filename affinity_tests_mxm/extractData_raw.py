#!/usr/bin/python

import os
import re
import numpy as np
#import statistics as st

test_name = 'output_20210623_142829'

# name of the new csv file (overwrites existing file)
filename = test_name + '_raw.csv'
# name of the directory where the .txt files from the slurm job are
# has to be in the same dir as this .py script
outputs_dir = 'outputs/' + test_name
logs_dir = outputs_dir + '/logs'

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
    ["OMP_NUM_THREADS", "OmpNumThreads"],
    ["AUTOMATIC_NUMA_BALANCING", "NumaBalancing"],
    ["Task Domain Hitrate", "StatDomainHitrate"], #All those "Stat" values get calculated per node
    ["Task gtid Hitrate", "StatGtidHitrate"],
    ["The domain changed", "StatDomainChanges"],
    ["The domain stayed the same", "StatDomainNotChanges"],
    ["The gtid changed", "StatGtidChanges"],
    ["The gtid stayed the same", "StatGtidNotChanges"],
    ["MXM_PARAMS", "MatrixSize,MatrixNumTasks,MatrixDistribution"],
    ["CHAMELEON_VERSION", "ChameleonVersion"],
    ["PROG", "Program"],
    ["Computations with chameleon took", "Time"],
    ["Computations with chameleon took", "TimeChameleon"],
    ["Computations with normal tasking took", "TimeTasking"],
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
def getTimeStatisticsOfDir(cur_log_dir_path, find_this_string):
    i = 0
    #times = [0.0]*len(os.listdir(cur_log_dir_path))
    times = np.zeros(len(os.listdir(cur_log_dir_path)))
    for read_file in os.listdir(cur_log_dir_path):
        found = False
        with open(os.path.join(cur_log_dir_path, read_file), 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.rstrip()
                param_found = re.findall(find_this_string, line)
                if len(param_found) == 0: continue
                else:
                    # Get the value of the string 
                    # (the first element after the string without [spaces, new lines, =])
                    start = line.find(find_this_string)
                    end = start + len(find_this_string)
                    res = line[end:].strip('%=\n\r ')
                    res_split = res.split(" ")
                    times[i] = float(res_split[0])
                    found = True
                    break
            if not found:
                times[i]=-1
            i += 1
    #times_median = st.median(times)
    times_median = np.median(times)
    uq = np.percentile(times, 75)
    lq = np.percentile(times, 25)
    iqr = uq - lq
    uw = times[times<=uq+1.5*iqr].max()
    lw = times[times>=lq-1.5*iqr].min()
    csv_file.write(str(times_median)+","+str(uq)+","+str(lq)+","+str(uw)+","+str(lw))

def getPerNodeStatisticsOfDir(cur_log_dir_path, find_this_string):
    i = 0
    stats = np.zeros(len(os.listdir(cur_log_dir_path)))
    for read_file in os.listdir(cur_log_dir_path):
        found = False
        found_counter = 0
        stats[i] = 0.0
        with open(os.path.join(cur_log_dir_path, read_file), 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.rstrip()
                param_found = re.findall(find_this_string, line)
                if len(param_found) == 0: continue
                else:
                    # Get the value of the string 
                    # (the first element after the string without [spaces, new lines, =])
                    start = line.find(find_this_string)
                    end = start + len(find_this_string)
                    res = line[end:].strip('%=\n\r ')
                    res_split = res.split(" ")
                    stats[i] += float(res_split[0])
                    found = True
                    found_counter += 1
                    continue # multiple values of stat per file
            if not found:
                stats[i]=-1
            else:
                stats[i] = stats[i]/found_counter # average of values per file
            i += 1
    stats_average = np.average(stats)
    csv_file.write(str(stats_average))

def getParametersOfDir(cur_log_dir_path):
    for read_file in os.listdir(cur_log_dir_path):
        with open(os.path.join(cur_log_dir_path, read_file), 'r') as f:
            lines = f.readlines()
            for string_idx in range(len(find_string)):
                # skip part that will be automatically calculated e.g. when calculating time
                if(find_string[string_idx][0] == "-"):
                    continue
                found = False
                if(find_string[string_idx][1].startswith('Stat')):
                    # the Stat values get calculated per node, i.e. occur multiple times per log file
                    getPerNodeStatisticsOfDir(cur_log_dir_path, find_string[string_idx][0])
                else:
                    for line in lines:
                        line = line.rstrip()
                        param_found = re.findall(find_string[string_idx][0], line)
                        if len(param_found) == 0: continue
                        else:
                            if param_found[0]=="MXM_PARAMS":
                                # Split up the Matrix parameters
                                start = line.find(find_string[string_idx][0])
                                end = start + len(find_string[string_idx][0])
                                res = line[end:].strip('%=\n\r ')
                                res_split = map(int, res.split(" "))
                                matrix_size = res_split[0]
                                matrix_task_dist = res_split[1:]
                                matrix_num_tasks = sum(matrix_task_dist)
                                matrix_task_dist_str = ""
                                for i in range(len(matrix_task_dist)):
                                    matrix_task_dist_str += str(matrix_task_dist[i])+" "
                                matrix_task_dist_str = matrix_task_dist_str.rstrip()
                                csv_file.write(str(matrix_size)+","+str(matrix_num_tasks)+","+matrix_task_dist_str)
                                found = True
                                break
                            else:
                                # Get the value of the string 
                                # (the first element after the string without [spaces, new lines, =])
                                start = line.find(find_string[string_idx][0])
                                end = start + len(find_string[string_idx][0])
                                res = line[end:].strip('%=\n\r ')
                                res_split = res.split(" ")
                                csv_file.write(res_split[0])
                                found = True
                                break
                    if not found:
                        # Parameter not in the file
                        if find_string[string_idx][1]=="Time":
                            # non chameleon version, find other time
                            other_time_string = "Computations with normal tasking took"
                            for line in lines:
                                line = line.rstrip()
                                param_found = re.findall(other_time_string, line)
                                if len(param_found) == 0: continue
                                else:
                                    # Get the value of the string 
                                    # (the first element after the string without [spaces, new lines, =])
                                    start = line.find(other_time_string)
                                    end = start + len(other_time_string)
                                    res = line[end:].strip('%=\n\r ')
                                    res_split = res.split(" ")
                                    csv_file.write(res_split[0])
                                    found = True
                                    break
                        if not found:
                            csv_file.write("-1")
                csv_file.write(",")
        # delete last character of line (which is a ",")
        csv_file.seek(-1,os.SEEK_END)
        csv_file.truncate()

        csv_file.write("\n")
    
####################################################
####################################################
####################################################

for cur_log_dir in os.listdir(logs_path):
    cur_log_dir_path = os.path.join(logs_path, cur_log_dir)
    getParametersOfDir(cur_log_dir_path)
    


# for read_file in os.listdir(outputs_path):
#     with open(os.path.join(outputs_path, read_file), 'r') as f:
#         lines = f.readlines()
#         for string_idx in range(len(find_string)):
#             found = False
#             for line in lines:
#                 line = line.rstrip()
#                 param_found = re.findall(find_string[string_idx][0], line)
#                 if len(param_found) == 0: continue
#                 else:
#                     if param_found[0]=="MXM_PARAMS":
#                         # Split up the Matrix parameters
#                         start = line.find(find_string[string_idx][0])
#                         end = start + len(find_string[string_idx][0])
#                         res = line[end:].strip('%=\n\r ')
#                         res_split = map(int, res.split(" "))
#                         matrix_size = res_split[0]
#                         matrix_task_dist = res_split[1:]
#                         matrix_num_tasks = sum(matrix_task_dist)
#                         matrix_task_dist_str = ""
#                         for i in range(len(matrix_task_dist)):
#                             matrix_task_dist_str += str(matrix_task_dist[i])+" "
#                         matrix_task_dist_str = matrix_task_dist_str.rstrip()
#                         csv_file.write(str(matrix_size)+","+str(matrix_num_tasks)+","+matrix_task_dist_str)
#                         if string_idx < len(find_string)-1:
#                             csv_file.write(",")
#                         found = True
#                         break
#                     else:
#                         # Get the value of the string 
#                         # (the first element after the string without [spaces, new lines, =])
#                         start = line.find(find_string[string_idx][0])
#                         end = start + len(find_string[string_idx][0])
#                         res = line[end:].strip('%=\n\r ')
#                         res_split = res.split(" ")
#                         csv_file.write(res_split[0])
#                         if string_idx < len(find_string)-1:
#                             csv_file.write(",")
#                         found = True
#                         break
#             if not found:
#                 csv_file.write("-1,")
#     csv_file.write("\n")

csv_file.close()