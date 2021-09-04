#!/usr/bin/python

import os
import re
import numpy as np
#import statistics as st
import csv

test_name = 'ContributionVariation_3Threads_20210903_144258'
outDir_name = test_name
# test_name = 'ChamStats_'+test_name

# name of the new csv file (overwrites existing file)
filename = test_name + '.csv'
# name of the directory where the .txt files from the slurm job are
# has to be in the same dir as this .py script
outputs_dir = 'outputs/' + outDir_name
logs_dir = outputs_dir + '/logs'
# find_string = [
#     ["REGION", "Region"], # 0 = 0 hops, 1 = 2 hops, 2 = 4 hops
#     ["PingPong with msg_size: 4 \( 0.004 KB\) took","Latency"],
#     ["PingPong with msg_size: 268435456 \( 262144.000 KB\) took","256MB_time"],
#     ["PingPong with msg_size: 268435456 \( 262144.000 KB\) took (\d)+\D(\d)+ us with a throughput of","256MB_throughput"],
# ]

computeTimeStats = False

find_string = [
    # Affinity Settings
    # ["CHAM_AFF_TASK_SELECTION_STRAT", "TaskSelectionStrat"],
    # ["CHAM_AFF_PAGE_SELECTION_STRAT", "PageSelectionStrat"],
    # ["CHAM_AFF_PAGE_WEIGHTING_STRAT", "PageWeightStrat"],
    # ["CHAM_AFF_CONSIDER_TYPES", "ConsiderTypes",],
    # ["CHAM_AFF_PAGE_SELECTION_N", "PageN"],
    # ["CHAM_AFF_TASK_SELECTION_N", "TaskN"],
    # ["CHAM_AFF_MAP_MODE", "MapMode"],
    # ["CHAM_AFF_ALWAYS_CHECK_PHYSICAL", "CheckPhysical"],
    # # SLURM information
    ["SLURM_JOB_NUM_NODES", "SlurmNodes"],
    ["SLURM_NTASKS_PER_NODE", "SlurmTasksPerNode"],
    ["OMP_NUM_THREADS", "OmpNumThreads"],
    # ["AUTOMATIC_NUMA_BALANCING", "NumaBalancing"],
    ["CHAM_COMMTHREAD_WORKCONTRIBUTION_LIMIT","CommThreadWorkContributionLimit"],
    ["MXM_PARAMS", "MatrixSize,MatrixNumTasks,MatrixDistribution"],
    ["CHAMELEON_VERSION", "ChameleonVersion"],
    # ["PROG", "Program"],
    # ["NODELIST","Nodelist"],
    # # runtime
    # topology settings
    # ["TOPO_MIGRATION_STRAT","TopoStrat"],
    # ["MIGRATION_OFFLOAD_TO_SINGLE_RANK","TopoOffloadSingle"],
    ["N_RUNS", "NRuns"], # Number of repetitions per scenario
    # # Likwid
    # ["L2 miss ratio STAT", "Likwid_L2MissRatio"],
    # ["L3 miss ratio STAT", "Likwid_L3MissRatio"],
    # ["Runtime \(RDTSC\) \[s\] STAT", "Likwid_Runtime"], # don't know what time this is, seems to be not usefull for me
    # ["Clock \[MHz\] STAT", "Likwid_Clock"], # probably not usefull for me
    # ["VARIATION_NAME","VariationName"],
    ["Computations with chameleon took", "TimeChameleon"],
    # ["-", "TCUQ"], # Time Chameleon Upper Quartile
    # ["-", "TCLQ"], # Time Chameleon Lower Quartile
    # ["-", "TCUW"], # Time Chameleon Upper Whisker
    # ["-", "TCLW"], # Time Chameleon Lower Whisker
    # ["Computations with normal tasking took", "TimeTasking"],
    # ["-", "TTUQ"], # Time Tasking Upper Quartile
    # ["-", "TTLQ"], # Time Tasking Lower Quartile
    # ["-", "TTUW"], # Time Tasking Upper Whisker
    # ["-", "TTLW"], # Time Tasking Lower Whisker
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
    # ["_num_migration_decision_performed","SUM_NumMigrationDecisionsPerformed"],
    # ["_num_migration_done","SUM_NumMigrationsDone"],
    # ["_num_tasks_executed_by_commthread","SUM_TasksExecutedByCommThread"],
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
def getNumLogs(cur_log_dir_path):
    num_of_files = 0
    for file in os.listdir(cur_log_dir_path):
        if file.endswith(".log"):
            num_of_files += 1
    return num_of_files

def getTimeStatisticsOfDir(cur_log_dir_path, find_this_string):
    i = 0
    times = np.zeros(getNumLogs(cur_log_dir_path))
    for read_file in os.listdir(cur_log_dir_path):
        # skip if not a log file
        if not read_file.endswith(".log"):
            continue
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
    if computeTimeStats:
        csv_file.write(str(times_median)+","+str(uq)+","+str(lq)+","+str(uw)+","+str(lw))
    else:
        csv_file.write(str(times_median))

def getMeanOfDir(cur_log_dir_path, find_this_string):
    i = 0
    # num of .log should be equal to num of .csv
    stats_array = np.zeros(getNumLogs(cur_log_dir_path))
    for read_file in os.listdir(cur_log_dir_path):
        # skip if not a csv file
        if not read_file.endswith(".log"):
            continue
        found = False
        with open(os.path.join(cur_log_dir_path, read_file), 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace('\t',' ').rstrip()
                param_found = re.findall(find_this_string, line)
                if len(param_found) == 0: continue
                else:
                    end = re.search(find_this_string,line).span()[1]
                    res = line[end:].replace('\t',' ').strip('%=\n\r\t ')
                    res_split = res.split(" ")
                    res_split[0]=res_split[0].replace(",","_")
                    stats_array[i] = float(res_split[0])
                    found = True
                    break
            if not found:
                stats_array[i]=-1
            i += 1
    stats_mean = np.median(stats_array)
    csv_file.write(str(stats_mean))

# mode 0: average stats of each file, mode 1: sum up stats per file
def getPerNodeStatisticsOfDir(cur_log_dir_path, find_this_string, mode=0):
    i = 0
    stats = np.zeros(getNumLogs(cur_log_dir_path))
    for read_file in os.listdir(cur_log_dir_path):
        # skip if not a log file
        if not read_file.endswith(".log"):
            continue
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
                if mode == 0:
                    stats[i] = stats[i]/found_counter # average of values per file
            i += 1
    stats_average = np.average(stats)
    csv_file.write(str(stats_average))

def getLikwidStatisticsOfDir(cur_log_dir_path, find_this_string):
    i = 0
    # num of .log should be equal to num of .csv
    stats_array = np.zeros(getNumLogs(cur_log_dir_path))
    for read_file in os.listdir(cur_log_dir_path):
        # skip if not a csv file
        if not read_file.endswith(".csv"):
            continue
        found = False
        with open(os.path.join(cur_log_dir_path, read_file), 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.rstrip()
                param_found = re.findall(find_this_string, line)
                if len(param_found) == 0: continue
                else:
                    # Get the value of the string 
                    line_array = line.split(",")
                    line_array = [line_iterator.strip(' ') for line_iterator in line_array]
                    # 4th column is the average for cache miss rate
                    stats_array[i] = float(line_array[4])
                    found = True
                    break
            if not found:
                stats_array[i]=-1
            i += 1
    stats_average = np.average(stats_array)
    csv_file.write(str(stats_average))

def getParametersOfDir(cur_log_dir_path):
    # get parameters (all except the time) from some file
    # find first log file
    for first_file in os.listdir(cur_log_dir_path):
        if first_file.endswith(".log"):
            # print("first_file before breaking foor loop:"+first_file)
            break
    # print("first_file after breaking foor loop:"+first_file)
    with open(os.path.join(cur_log_dir_path, first_file), 'r') as f:
        lines = f.readlines()
        for string_idx in range(len(find_string)):
            # skip part that will be automatically calculated e.g. when calculating time
            if(find_string[string_idx][0] == "-"):
                continue
            found = False
            if(find_string[string_idx][1].startswith('Time')):
                # has to iterate over all runs to get the median,... of the times
                getTimeStatisticsOfDir(cur_log_dir_path, find_string[string_idx][0])
            elif(find_string[string_idx][1].startswith('R')):
                # has to iterate over all runs to get the median,... of the stats
                getMeanOfDir(cur_log_dir_path, find_string[string_idx][0])
            elif(find_string[string_idx][1].startswith('Stat')):
                # the Stat values get calculated per node, i.e. occur multiple times per log file
                getPerNodeStatisticsOfDir(cur_log_dir_path, find_string[string_idx][0],0) # avg per file
            elif(find_string[string_idx][1].startswith('SUM')):
                getPerNodeStatisticsOfDir(cur_log_dir_path, find_string[string_idx][0],1) # sum per file
            elif(find_string[string_idx][1].startswith('Likwid')):
                # get the likwid stats from the .csv files
                getLikwidStatisticsOfDir(cur_log_dir_path, find_string[string_idx][0])
            else:
                for line in lines:
                    line = line.replace('\t',' ').rstrip()
                    param_found = re.findall(find_string[string_idx][0], line)
                    if len(param_found) == 0: continue
                    else:
                        # print("Found something: "+line+"\n")
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

for cur_log_dir in os.listdir(logs_path):
    cur_log_dir_path = os.path.join(logs_path, cur_log_dir)
    getParametersOfDir(cur_log_dir_path)
    # delete last character of line (which is a ",")
    csv_file.seek(-1,os.SEEK_END)
    csv_file.truncate()

    csv_file.write("\n")

csv_file.close()

####################################################
#               Order file                         #
####################################################

# rowNames=['Variation','SomeIndex','Group']
rowNames=['SomeIndex','Group']

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
