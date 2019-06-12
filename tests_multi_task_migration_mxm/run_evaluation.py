import os #, sys
import numpy as np
import statistics as st
from datetime import datetime
import csv
from CResult import *
import numpy as np
import matplotlib.pyplot as plt

def plotData(target_file_path, arr_x_axis, arr_types, arr_time_baseline, arr_time_chameleon, arr_remote_tasks, text_header, text_x_axis):
    xtick = list(range(len(arr_x_axis)))

    # ========== Time Plot
    path_result_img = target_file_path + "_time.png"
    fig = plt.figure(figsize=(16, 9))
    ax = fig.gca()
    # baseline first
    labels = ['OpenMP baseline']
    ax.plot(xtick, np.array(arr_time_baseline[0]), 'x-', linewidth=2)
    # now versions
    for idx_type in range(len(arr_types)):
        ax.plot(xtick, np.array(arr_time_chameleon[idx_type]), 'x-', linewidth=2)
        labels.append(arr_types[idx_type])
    plt.xticks(xtick, arr_x_axis)
    ax.minorticks_on()
    ax.legend(labels, fancybox=True, shadow=False)                
    ax.grid(b=True, which='major', axis="both", linestyle='-', linewidth=1)
    ax.grid(b=True, which='minor', axis="both", linestyle='-', linewidth=0.4)
    ax.set_xlabel(text_x_axis)
    ax.set_ylabel("Time [sec]")
    ax.set_title(text_header + " - Execution Time" )
    fig.savefig(path_result_img, dpi=None, facecolor='w', edgecolor='w', 
        format="png", transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)
    plt.close(fig)

    # ========== Speedup Plot
    path_result_img = target_file_path + "_speedup.png"
    fig = plt.figure(figsize=(16, 9))
    ax = fig.gca()
    # baseline first
    labels = ['OpenMP baseline']
    ax.plot(xtick, np.array([1 for x in xtick]), 'x-', linewidth=2)
    # now versions
    for idx_type in range(len(arr_types)):
        tmp_speedups = [arr_time_baseline[0][x] / arr_time_chameleon[idx_type][x] for x in range(len(arr_x_axis))]
        ax.plot(xtick, np.array(tmp_speedups), 'x-', linewidth=2)
        labels.append(arr_types[idx_type])
    plt.xticks(xtick, arr_x_axis)
    ax.minorticks_on()
    ax.legend(labels, fancybox=True, shadow=False)
    ax.grid(b=True, which='major', axis="both", linestyle='-', linewidth=1)
    ax.grid(b=True, which='minor', axis="both", linestyle='-', linewidth=0.4)
    ax.set_xlabel(text_x_axis)
    ax.set_ylabel("Speedup")
    ax.set_title(text_header + " - Speedup" )
    fig.savefig(path_result_img, dpi=None, facecolor='w', edgecolor='w', 
        format="png", transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)
    plt.close(fig)

    # ========== Number of migrated tasks
    path_result_img = target_file_path + "_migrated.png"
    fig = plt.figure(figsize=(16, 9))
    ax = fig.gca()
    labels = ['OpenMP baseline']
    ax.plot(xtick, np.array([0 for x in xtick]), 'x-', linewidth=2)
    # now versions
    for idx_type in range(len(arr_types)):
        ax.plot(xtick, np.array(arr_remote_tasks[idx_type]), 'x-', linewidth=2)
        labels.append(arr_types[idx_type])
    plt.xticks(xtick, arr_x_axis)
    ax.minorticks_on()
    ax.legend(labels, fancybox=True, shadow=False)
    ax.grid(b=True, which='major', axis="both", linestyle='-', linewidth=1)
    ax.grid(b=True, which='minor', axis="both", linestyle='-', linewidth=0.4)
    ax.set_xlabel(text_x_axis)
    ax.set_ylabel("# migrated tasks")
    ax.set_title(text_header + " - Migrated Tasks" )
    fig.savefig(path_result_img, dpi=None, facecolor='w', edgecolor='w', 
        format="png", transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)
    plt.close(fig)

if __name__ == "__main__":
    # source_folder = os.path.dirname(os.path.abspath(__file__))
    source_folder       = "C:\\J.Klinkenberg.Local\\repos\\chameleon\\chameleon-scripts\\tests_multi_task_migration_mxm\\results_8nodes_dm"
    target_folder_data  = os.path.join(source_folder, "result_data")
    target_folder_plot  = os.path.join(source_folder, "result_plots")

    # create target directories of not yet existing
    if not os.path.exists(target_folder_data):
        os.makedirs(target_folder_data)
    if not os.path.exists(target_folder_plot):
        os.makedirs(target_folder_plot)

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

        # output results
        tmp_target_file_name = "output_granularity_" + str(gran) + ".result"
        tmp_target_file_path = os.path.join(target_folder_data, tmp_target_file_name)
        with open(tmp_target_file_path, mode='w', newline='') as f:
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

        # plot results
        tmp_target_file_name = "plot_granularity_" + str(int(gran))
        tmp_target_file_path = os.path.join(target_folder_plot, tmp_target_file_name)
        plotData(tmp_target_file_path, unique_n_threads, arr_types, arr_time_original, arr_time_chameleon, arr_n_tasks_remote, "Granularity " + str(int(gran)), "# threads per rank")

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

        # output results
        tmp_target_file_name = "output_thread_" + str(thr) + ".result"
        tmp_target_file_path = os.path.join(target_folder_data, tmp_target_file_name)
        with open(tmp_target_file_path, mode='w', newline='') as f:
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
            writer.writerow(['N_LocalTasks'] + unique_granularities)
            for tmp_idx in range(len(arr_types)):
                writer.writerow([arr_types[tmp_idx]] + arr_n_tasks_local[tmp_idx])
            writer.writerow([])
            writer.writerow(['N_RemoteTasks'] + unique_granularities)
            for tmp_idx in range(len(arr_types)):
                writer.writerow([arr_types[tmp_idx]] + arr_n_tasks_remote[tmp_idx])

        # plot results
        tmp_target_file_name = "plot_threads_" + str(int(thr))
        tmp_target_file_path = os.path.join(target_folder_plot, tmp_target_file_name)
        plotData(tmp_target_file_path, unique_granularities, arr_types, arr_time_original, arr_time_chameleon, arr_n_tasks_remote, str(int(thr)) + " Threads", "# task granularity (matrix size)")