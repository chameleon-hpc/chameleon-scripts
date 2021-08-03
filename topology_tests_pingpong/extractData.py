#!/usr/bin/python

import os
import re
import numpy as np
#import statistics as st

test_name = 'RegionsPingPong_20210731_135723'

# name of the new csv file (overwrites existing file)
filename = test_name + '.csv'
# name of the directory where the .txt files from the slurm job are
# has to be in the same dir as this .py script
outputs_dir = 'outputs/' + test_name
logs_dir = outputs_dir + '/logs'
find_string = [
    ["REGION", "Region"], # 0 = 0 hops, 1 = 2 hops, 2 = 4 hops
    ["PingPong with msg_size: 4 \( 0.004 KB\) took","4B_time"],
    ["PingPong with msg_size: 8 \( 0.008 KB\) took","8B_time"],
    ["PingPong with msg_size: 16 \( 0.016 KB\) took","16B_time"],
    ["PingPong with msg_size: 32 \( 0.031 KB\) took","32B_time"],
    ["PingPong with msg_size: 64 \( 0.062 KB\) took","64B_time"],
    ["PingPong with msg_size: 128 \( 0.125 KB\) took","128B_time"],
    ["PingPong with msg_size: 256 \( 0.250 KB\) took","256B_time"],
    ["PingPong with msg_size: 512 \( 0.500 KB\) took","512B_time"],
    ["PingPong with msg_size: 1024 \( 1.000 KB\) took","1KB_time"],
    ["PingPong with msg_size: 2048 \( 2.000 KB\) took","2KB_time"],
    ["PingPong with msg_size: 4096 \( 4.000 KB\) took","4KB_time"],
    ["PingPong with msg_size: 8192 \( 8.000 KB\) took","8KB_time"],
    ["PingPong with msg_size: 16384 \( 16.000 KB\) took","16KB_time"],
    ["PingPong with msg_size: 32768 \( 32.000 KB\) took","32KB_time"],
    ["PingPong with msg_size: 65536 \( 64.000 KB\) took","64KB_time"],
    ["PingPong with msg_size: 131072 \( 128.000 KB\) took","128KB_time"],
    ["PingPong with msg_size: 262144 \( 256.000 KB\) took","256KB_time"],
    ["PingPong with msg_size: 524288 \( 512.000 KB\) took","512KB_time"],
    ["PingPong with msg_size: 1048576 \( 1024.000 KB\) took","1MB_time"],
    ["PingPong with msg_size: 2097152 \( 2048.000 KB\) took","2MB_time"],
    ["PingPong with msg_size: 4194304 \( 4096.000 KB\) took","4MB_time"],
    ["PingPong with msg_size: 8388608 \( 8192.000 KB\) took","8MB_time"],
    ["PingPong with msg_size: 16777216 \( 16384.000 KB\) took","16MB_time"],
    ["PingPong with msg_size: 33554432 \( 32768.000 KB\) took","32MB_time"],
    ["PingPong with msg_size: 67108864 \( 65536.000 KB\) took","64MB_time"],
    ["PingPong with msg_size: 134217728 \( 131072.000 KB\) took","128MB_time"],
    ["PingPong with msg_size: 268435456 \( 262144.000 KB\) took","256MB_time"],
    ["PingPong with msg_size: 4 \( 0.004 KB\) took (\d)+\D(\d)+ us with a throughput of","4B_throughput"],
    ["PingPong with msg_size: 8 \( 0.008 KB\) took (\d)+\D(\d)+ us with a throughput of","8B_throughput"],
    ["PingPong with msg_size: 16 \( 0.016 KB\) took (\d)+\D(\d)+ us with a throughput of","16B_throughput"],
    ["PingPong with msg_size: 32 \( 0.031 KB\) took (\d)+\D(\d)+ us with a throughput of","32B_throughput"],
    ["PingPong with msg_size: 64 \( 0.062 KB\) took (\d)+\D(\d)+ us with a throughput of","64B_throughput"],
    ["PingPong with msg_size: 128 \( 0.125 KB\) took (\d)+\D(\d)+ us with a throughput of","128B_throughput"],
    ["PingPong with msg_size: 256 \( 0.250 KB\) took (\d)+\D(\d)+ us with a throughput of","256B_throughput"],
    ["PingPong with msg_size: 512 \( 0.500 KB\) took (\d)+\D(\d)+ us with a throughput of","512B_throughput"],
    ["PingPong with msg_size: 1024 \( 1.000 KB\) took (\d)+\D(\d)+ us with a throughput of","1KB_throughput"],
    ["PingPong with msg_size: 2048 \( 2.000 KB\) took (\d)+\D(\d)+ us with a throughput of","2KB_throughput"],
    ["PingPong with msg_size: 4096 \( 4.000 KB\) took (\d)+\D(\d)+ us with a throughput of","4KB_throughput"],
    ["PingPong with msg_size: 8192 \( 8.000 KB\) took (\d)+\D(\d)+ us with a throughput of","8KB_throughput"],
    ["PingPong with msg_size: 16384 \( 16.000 KB\) took (\d)+\D(\d)+ us with a throughput of","16KB_throughput"],
    ["PingPong with msg_size: 32768 \( 32.000 KB\) took (\d)+\D(\d)+ us with a throughput of","32KB_throughput"],
    ["PingPong with msg_size: 65536 \( 64.000 KB\) took (\d)+\D(\d)+ us with a throughput of","64KB_throughput"],
    ["PingPong with msg_size: 131072 \( 128.000 KB\) took (\d)+\D(\d)+ us with a throughput of","128KB_throughput"],
    ["PingPong with msg_size: 262144 \( 256.000 KB\) took (\d)+\D(\d)+ us with a throughput of","256KB_throughput"],
    ["PingPong with msg_size: 524288 \( 512.000 KB\) took (\d)+\D(\d)+ us with a throughput of","512KB_throughput"],
    ["PingPong with msg_size: 1048576 \( 1024.000 KB\) took (\d)+\D(\d)+ us with a throughput of","1MB_throughput"],
    ["PingPong with msg_size: 2097152 \( 2048.000 KB\) took (\d)+\D(\d)+ us with a throughput of","2MB_throughput"],
    ["PingPong with msg_size: 4194304 \( 4096.000 KB\) took (\d)+\D(\d)+ us with a throughput of","4MB_throughput"],
    ["PingPong with msg_size: 8388608 \( 8192.000 KB\) took (\d)+\D(\d)+ us with a throughput of","8MB_throughput"],
    ["PingPong with msg_size: 16777216 \( 16384.000 KB\) took (\d)+\D(\d)+ us with a throughput of","16MB_throughput"],
    ["PingPong with msg_size: 33554432 \( 32768.000 KB\) took (\d)+\D(\d)+ us with a throughput of","32MB_throughput"],
    ["PingPong with msg_size: 67108864 \( 65536.000 KB\) took (\d)+\D(\d)+ us with a throughput of","64MB_throughput"],
    ["PingPong with msg_size: 134217728 \( 131072.000 KB\) took (\d)+\D(\d)+ us with a throughput of","128MB_throughput"],
    ["PingPong with msg_size: 268435456 \( 262144.000 KB\) took (\d)+\D(\d)+ us with a throughput of","256MB_throughput"],
    ["N_RUNS", "NRuns"], # Number of repetitions per scenario
]
# find_string = [
#     ["CHAM_AFF_TASK_SELECTION_STRAT", "TaskSelectionStrat"],
#     ["CHAM_AFF_PAGE_SELECTION_STRAT", "PageSelectionStrat"],
#     ["CHAM_AFF_PAGE_WEIGHTING_STRAT", "PageWeightStrat"],
#     ["CHAM_AFF_CONSIDER_TYPES", "ConsiderTypes",],
#     ["CHAM_AFF_PAGE_SELECTION_N", "PageN"],
#     ["CHAM_AFF_TASK_SELECTION_N", "TaskN"],
#     ["CHAM_AFF_MAP_MODE", "MapMode"],
#     ["CHAM_AFF_ALWAYS_CHECK_PHYSICAL", "CheckPhysical"],
#     ["SLURM_JOB_NUM_NODES", "SlurmNodes"],
#     ["SLURM_NTASKS_PER_NODE", "SlurmTasksPerNode"],
#     ["OMP_NUM_THREADS", "OmpNumThreads"],
#     ["AUTOMATIC_NUMA_BALANCING", "NumaBalancing"],
#     ["Task Domain Hitrate", "StatDomainHitrate"], #All those "Stat" values get calculated per node
#     ["Task gtid Hitrate", "StatGtidHitrate"],
#     ["The domain changed", "StatDomainChanges"],
#     ["The domain stayed the same", "StatDomainNotChanges"],
#     ["The gtid changed", "StatGtidChanges"],
#     ["The gtid stayed the same", "StatGtidNotChanges"],
#     ["MXM_PARAMS", "MatrixSize,MatrixNumTasks,MatrixDistribution"],
#     ["CHAMELEON_VERSION", "ChameleonVersion"],
#     ["PROG", "Program"],
#     ["Computations with chameleon took", "TimeChameleon"],
#     ["-", "TCUQ"], # Time Chameleon Upper Quartile
#     ["-", "TCLQ"], # Time Chameleon Lower Quartile
#     ["-", "TCUW"], # Time Chameleon Upper Whisker
#     ["-", "TCLW"], # Time Chameleon Lower Whisker
#     ["Computations with normal tasking took", "TimeTasking"],
#     ["-", "TTUQ"], # Time Tasking Upper Quartile
#     ["-", "TTLQ"], # Time Tasking Lower Quartile
#     ["-", "TTUW"], # Time Tasking Upper Whisker
#     ["-", "TTLW"], # Time Tasking Lower Whisker
#     ["N_RUNS", "NRuns"], # Number of repetitions per scenario
#     ["L2 miss ratio STAT", "Likwid_L2MissRatio"],
#     ["L3 miss ratio STAT", "Likwid_L3MissRatio"],
#     ["Runtime \(RDTSC\) \[s\] STAT", "Likwid_Runtime"], # don't know what time this is, seems to be not usefull for me
#     ["Clock \[MHz\] STAT", "Likwid_Clock"], # probably not usefull for me
#     ["SOME_INDEX", "SomeIndex"],    # Index for simpler Plotting
#     ]

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
    times = np.zeros(len(os.listdir(cur_log_dir_path))/2)
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
    csv_file.write(str(times_median)+","+str(uq)+","+str(lq)+","+str(uw)+","+str(lw))

def getPerNodeStatisticsOfDir(cur_log_dir_path, find_this_string):
    i = 0
    # dirs/2 because each log has its likwid csv file
    stats = np.zeros(len(os.listdir(cur_log_dir_path))/2)
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
                stats[i] = stats[i]/found_counter # average of values per file
            i += 1
    stats_average = np.average(stats)
    csv_file.write(str(stats_average))

def getLikwidStatisticsOfDir(cur_log_dir_path, find_this_string):
    i = 0
    stats_array = np.zeros(len(os.listdir(cur_log_dir_path))/2)
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
            break
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
            elif(find_string[string_idx][1].startswith('Stat')):
                # the Stat values get calculated per node, i.e. occur multiple times per log file
                getPerNodeStatisticsOfDir(cur_log_dir_path, find_string[string_idx][0])
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