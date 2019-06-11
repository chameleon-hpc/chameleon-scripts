import os #, sys
import numpy as np
import statistics as st
from datetime import datetime
import csv
from CResult import *

if __name__ == "__main__":
    source_folder = os.path.dirname(os.path.abspath(__file__))

    # list of result containers
    list_results = []

    # parse results
    for file in os.listdir(source_folder):
        if file.endswith(".log"):
            print(os.path.join(source_folder, file))
            tmp_result = CResult()
            tmp_result.parseFile(os.path.join(source_folder, file))
            list_results.append(tmp_result)

    # get unique types
    unique_types = sorted(list(set([x.result_type for x in list_results])))
    # get unique number of threads
    unique_n_threads = sorted(list(set([x.n_threads for x in list_results])))
    # get unique number of threads
    unique_granularities = sorted(list(set([x.task_granularity for x in list_results])))

    # ========== Generate results with fixed task granularity
    for gran in unique_granularities:
        sub_list = [x for x in list_results if x.task_granularity == gran]
        
        arr_types               = []
        arr_time_original       = []
        arr_time_chameleon      = []
        arr_n_tasks_local       = []
        arr_n_tasks_remote      = []

        for ty in unique_types:
            tmp_list = [x for x in sub_list if x.result_type == ty]            
            if tmp_list:
                arr_types.append(ty)
                tmp_time_original   = [0 for x in unique_n_threads]
                tmp_time_chameleon  = [0 for x in unique_n_threads]
                tmp_n_tasks_local   = [0 for x in unique_n_threads]
                tmp_n_tasks_remote  = [0 for x in unique_n_threads]
                idx = 0
                for thr in unique_n_threads:
                    tmp_list_thr = [x for x in tmp_list if x.n_threads == thr]
                    # calculate mean values
                    cur_mean_ch             = st.mean([x.time_chameleon for x in tmp_list_thr])
                    cur_mean_orig           = st.mean([x.time_openmp_only for x in tmp_list_thr])
                    cur_mean_t_local        = st.mean([x.n_local_tasks for x in tmp_list_thr])
                    cur_mean_t_remote       = st.mean([x.n_remote_tasks for x in tmp_list_thr])
                    tmp_time_chameleon[idx] = cur_mean_ch
                    tmp_time_original[idx]  = cur_mean_orig
                    tmp_n_tasks_local[idx]  = cur_mean_t_local
                    tmp_n_tasks_remote[idx] = cur_mean_t_remote
                    idx = idx + 1
                # append arrays
                arr_time_original.append(tmp_time_original)
                arr_time_chameleon.append(tmp_time_chameleon)
                arr_n_tasks_local.append(tmp_n_tasks_local)
                arr_n_tasks_remote.append(tmp_n_tasks_remote)

        # output/plot results
        with open("output_granularity_" + str(gran) + ".result", mode='w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['OpenMP'] + unique_n_threads)
            for tmp_idx in range(len(arr_types)):
                writer.writerow([arr_types[tmp_idx]] + arr_time_original[tmp_idx])
            writer.writerow([])
            writer.writerow(['Chameleon'] + unique_n_threads)
            for tmp_idx in range(len(arr_types)):
                writer.writerow([arr_types[tmp_idx]] + arr_time_chameleon[tmp_idx])
            writer.writerow([])
            writer.writerow(['Speedup'] + unique_n_threads)
            for tmp_idx in range(len(arr_types)):
                tmp_speedups = [arr_time_original[0][x] / arr_time_chameleon[tmp_idx][x] for x in range(len(unique_n_threads))]
                writer.writerow([arr_types[tmp_idx]] + tmp_speedups)
            writer.writerow([])
            writer.writerow(['N_LocalTasks'] + unique_n_threads)
            for tmp_idx in range(len(arr_types)):
                writer.writerow([arr_types[tmp_idx]] + arr_n_tasks_local[tmp_idx])
            writer.writerow([])
            writer.writerow(['N_RemoteTasks'] + unique_n_threads)
            for tmp_idx in range(len(arr_types)):
                writer.writerow([arr_types[tmp_idx]] + arr_n_tasks_remote[tmp_idx])

    # ========== Generate results with fixed number of threads
    for thr in unique_n_threads:
        sub_list = [x for x in list_results if x.n_threads == thr]
        
        arr_types               = []
        arr_time_original       = []
        arr_time_chameleon      = []
        arr_n_tasks_local       = []
        arr_n_tasks_remote      = []

        for ty in unique_types:
            tmp_list = [x for x in sub_list if x.result_type == ty]            
            if tmp_list:
                arr_types.append(ty)
                tmp_time_original   = [0 for x in unique_granularities]
                tmp_time_chameleon  = [0 for x in unique_granularities]
                tmp_n_tasks_local   = [0 for x in unique_granularities]
                tmp_n_tasks_remote  = [0 for x in unique_granularities]
                idx = 0
                for gran in unique_granularities:
                    tmp_list_thr = [x for x in tmp_list if x.task_granularity == gran]
                    # calculate mean values
                    cur_mean_ch             = st.mean([x.time_chameleon for x in tmp_list_thr])
                    cur_mean_orig           = st.mean([x.time_openmp_only for x in tmp_list_thr])
                    cur_mean_t_local        = st.mean([x.n_local_tasks for x in tmp_list_thr])
                    cur_mean_t_remote       = st.mean([x.n_remote_tasks for x in tmp_list_thr])
                    tmp_time_chameleon[idx] = cur_mean_ch
                    tmp_time_original[idx]  = cur_mean_orig
                    tmp_n_tasks_local[idx]  = cur_mean_t_local
                    tmp_n_tasks_remote[idx] = cur_mean_t_remote
                    idx = idx + 1
                # append arrays
                arr_time_original.append(tmp_time_original)
                arr_time_chameleon.append(tmp_time_chameleon)
                arr_n_tasks_local.append(tmp_n_tasks_local)
                arr_n_tasks_remote.append(tmp_n_tasks_remote)

        # output/plot results
        with open("output_thread_" + str(thr) + ".result", mode='w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['OpenMP'] + unique_granularities)
            for tmp_idx in range(len(arr_types)):
                writer.writerow([arr_types[tmp_idx]] + arr_time_original[tmp_idx])
            writer.writerow([])
            writer.writerow(['Chameleon'] + unique_granularities)
            for tmp_idx in range(len(arr_types)):
                writer.writerow([arr_types[tmp_idx]] + arr_time_chameleon[tmp_idx])
            writer.writerow([])
            writer.writerow(['Speedup'] + unique_granularities)
            for tmp_idx in range(len(arr_types)):
                tmp_speedups = [arr_time_original[0][x] / arr_time_chameleon[tmp_idx][x] for x in range(len(unique_granularities))]
                writer.writerow([arr_types[tmp_idx]] + tmp_speedups)
            writer.writerow([])
            writer.writerow(['N_LocalTasks'] + unique_n_threads)
            for tmp_idx in range(len(arr_types)):
                writer.writerow([arr_types[tmp_idx]] + arr_n_tasks_local[tmp_idx])
            writer.writerow([])
            writer.writerow(['N_RemoteTasks'] + unique_n_threads)
            for tmp_idx in range(len(arr_types)):
                writer.writerow([arr_types[tmp_idx]] + arr_n_tasks_remote[tmp_idx])

