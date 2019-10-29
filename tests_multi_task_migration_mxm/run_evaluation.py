import os #, sys
import numpy as np
import statistics as st
from datetime import datetime
import csv
from CResult import *
import numpy as np
import matplotlib.pyplot as plt

F_SIZE = 16

plt.rc('font', size=F_SIZE)             # controls default text sizes
plt.rc('axes', titlesize=F_SIZE)        # fontsize of the axes title
plt.rc('axes', labelsize=F_SIZE)        # fontsize of the x and y labels
plt.rc('xtick', labelsize=F_SIZE)       # fontsize of the tick labels
plt.rc('ytick', labelsize=F_SIZE)       # fontsize of the tick labels
plt.rc('legend', fontsize=F_SIZE)       # legend fontsize
plt.rc('figure', titlesize=F_SIZE)      # fontsize of the figure title

def plotDataMinMaxAvg(target_file_path, arr_x_axis, arr_types, arr_min, arr_max, arr_avg, text_header, text_x_axis, text_y_axis, plot_per_type=False, divisor=None):
    xtick = list(range(len(arr_x_axis)))

    if divisor is not None:
        for idx_type in range(len(arr_types)):
            arr_min[idx_type] = [x/divisor for x in arr_min[idx_type]]
            arr_max[idx_type] = [x/divisor for x in arr_max[idx_type]]
            arr_avg[idx_type] = [x/divisor for x in arr_avg[idx_type]]

    tmp_colors = ['darkorange', 'green', 'red']

    # ========== MinMaxAvg Plot
    if plot_per_type:
        for idx_type in range(len(arr_types)):
            path_result_img = target_file_path + "_" + arr_types[idx_type] + ".png"
            fig = plt.figure(figsize=(16, 9),frameon=False)
            ax = fig.gca()
            labels = []
            cur_line = ax.plot(xtick, np.array(arr_min[idx_type]), ':', linewidth=2, color=tmp_colors[idx_type])
            cur_color = cur_line[0].get_color()
            labels.append(arr_types[idx_type] + "_min")
            cur_line = ax.plot(xtick, np.array(arr_max[idx_type]), '--', linewidth=2)
            cur_line[0].set_color(cur_color)
            labels.append(arr_types[idx_type] + "_max")
            cur_line = ax.plot(xtick, np.array(arr_avg[idx_type]), '-', linewidth=2)
            cur_line[0].set_color(cur_color)
            labels.append(arr_types[idx_type] + "_avg")
        
            plt.xticks(xtick, arr_x_axis)
            ax.minorticks_on()
            ax.legend(labels, fancybox=True, shadow=False)                
            ax.grid(b=True, which='major', axis="both", linestyle='-', linewidth=1)
            ax.grid(b=True, which='minor', axis="both", linestyle='-', linewidth=0.4)
            ax.set_xlabel(text_x_axis)
            ax.set_ylabel(text_y_axis)
            ax.set_title(text_header + " (" + arr_types[idx_type] + ")")
            fig.savefig(path_result_img, dpi=None, facecolor='w', edgecolor='w', 
                format="png", transparent=False, bbox_inches='tight', pad_inches=0,
                frameon=False, metadata=None)
            plt.close(fig) 
    else:
        path_result_img = target_file_path + ".png"
        fig = plt.figure(figsize=(16, 9),frameon=False)
        ax = fig.gca()
        labels = []
        # now versions
        for idx_type in range(len(arr_types)):
            cur_line = ax.plot(xtick, np.array(arr_min[idx_type]), ':', linewidth=2, color=tmp_colors[idx_type])
            cur_color = cur_line[0].get_color()
            labels.append(arr_types[idx_type] + "_min")
            cur_line = ax.plot(xtick, np.array(arr_max[idx_type]), '--', linewidth=2)
            cur_line[0].set_color(cur_color)
            labels.append(arr_types[idx_type] + "_max")
            cur_line = ax.plot(xtick, np.array(arr_avg[idx_type]), '-', linewidth=2)
            cur_line[0].set_color(cur_color)
            labels.append(arr_types[idx_type] + "_avg")
        plt.xticks(xtick, arr_x_axis)
        ax.minorticks_on()
        ax.legend(labels, fancybox=True, shadow=False)                
        ax.grid(b=True, which='major', axis="both", linestyle='-', linewidth=1)
        ax.grid(b=True, which='minor', axis="both", linestyle='-', linewidth=0.4)
        ax.set_xlabel(text_x_axis)
        ax.set_ylabel(text_y_axis)
        ax.set_title(text_header)
        fig.savefig(path_result_img, dpi=None, facecolor='w', edgecolor='w', 
            format="png", transparent=False, bbox_inches='tight', pad_inches=0,
            frameon=False, metadata=None)
        plt.close(fig)

def plotData(target_file_path, arr_x_axis, arr_types, arr_time_baseline, arr_time_chameleon, arr_remote_tasks, text_header, text_x_axis):
    xtick = list(range(len(arr_x_axis)))

    tmp_colors = ['darkorange', 'green', 'red']

    # ========== Time Plot
    path_result_img = target_file_path + "_time.png"
    fig = plt.figure(figsize=(16, 9),frameon=False)
    ax = fig.gca()
    # baseline first
    labels = ['OpenMP baseline']
    ax.plot(xtick, np.array(arr_time_baseline[0]), 'x-', linewidth=2)
    # now versions
    for idx_type in range(len(arr_types)):
        ax.plot(xtick, np.array(arr_time_chameleon[idx_type]), 'x-', linewidth=2, color=tmp_colors[idx_type])
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
        format="png", transparent=False, bbox_inches='tight', pad_inches=0,
        frameon=False, metadata=None)
    plt.close(fig)

    # ========== Speedup Plot
    path_result_img = target_file_path + "_speedup.png"
    fig = plt.figure(figsize=(16, 9),frameon=False)
    ax = fig.gca()
    # baseline first
    labels = ['OpenMP baseline']
    ax.plot(xtick, np.array([1 for x in xtick]), 'x-', linewidth=2)
    # now versions
    for idx_type in range(len(arr_types)):
        tmp_speedups = [arr_time_baseline[0][x] / arr_time_chameleon[idx_type][x] for x in range(len(arr_x_axis))]
        ax.plot(xtick, np.array(tmp_speedups), 'x-', linewidth=2, color=tmp_colors[idx_type])
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
        format="png", transparent=False, bbox_inches='tight', pad_inches=0,
        frameon=False, metadata=None)
    plt.close(fig)

    # ========== Number of migrated tasks
    path_result_img = target_file_path + "_migrated.png"
    fig = plt.figure(figsize=(16, 9),frameon=False)
    ax = fig.gca()
    labels = ['OpenMP baseline']
    ax.plot(xtick, np.array([0 for x in xtick]), 'x-', linewidth=2)
    # now versions
    for idx_type in range(len(arr_types)):
        ax.plot(xtick, np.array(arr_remote_tasks[idx_type]), 'x-', linewidth=2, color=tmp_colors[idx_type])
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
        format="png", transparent=False, bbox_inches='tight', pad_inches=0,
        frameon=False, metadata=None)
    plt.close(fig)

if __name__ == "__main__":
    # source_folder = os.path.dirname(os.path.abspath(__file__))
    source_folder       = "F:\\repos\\chameleon\\chameleon-scripts\\tests_multi_task_migration_mxm\\20191029_193654_results\\2procs_dm"
    target_folder_data  = os.path.join(source_folder, "result_data")
    target_folder_plot  = os.path.join(source_folder, "result_plots")

    # create target directories of not yet existing
    if not os.path.exists(target_folder_data):
        os.makedirs(target_folder_data)
    if not os.path.exists(target_folder_plot):
        os.makedirs(target_folder_plot)

    # get file name from path
    title_prefix = os.path.basename(source_folder)

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
        
        arr_types                   = []
        arr_time_original           = []
        arr_time_chameleon          = []
        arr_n_tasks_local           = []
        arr_n_tasks_remote          = []
        
        # used from first rank
        arr_bytes_send_per_msg_min  = []
        arr_bytes_send_per_msg_max  = []
        arr_bytes_send_per_msg_avg  = []
        arr_throughput_send_min     = []
        arr_throughput_send_max     = []
        arr_throughput_send_avg     = []

        # used from last rank
        arr_bytes_recv_per_msg_min  = []
        arr_bytes_recv_per_msg_max  = []
        arr_bytes_recv_per_msg_avg  = []
        arr_throughput_recv_min     = []
        arr_throughput_recv_max     = []
        arr_throughput_recv_avg     = []

        for ty in unique_types:
            tmp_list = [x for x in sub_list if x.result_type == ty]            
            if tmp_list:
                arr_types.append(ty)
                tmp_time_original   = [0 for x in unique_n_threads]
                tmp_time_chameleon  = [0 for x in unique_n_threads]
                tmp_n_tasks_local   = [0 for x in unique_n_threads]
                tmp_n_tasks_remote  = [0 for x in unique_n_threads]

                # used from first rank
                tmp_bytes_send_per_msg_min  = [0 for x in unique_n_threads]
                tmp_bytes_send_per_msg_max  = [0 for x in unique_n_threads]
                tmp_bytes_send_per_msg_avg  = [0 for x in unique_n_threads]
                tmp_throughput_send_min     = [0 for x in unique_n_threads]
                tmp_throughput_send_max     = [0 for x in unique_n_threads]
                tmp_throughput_send_avg     = [0 for x in unique_n_threads]

                # used from last rank
                tmp_bytes_recv_per_msg_min  = [0 for x in unique_n_threads]
                tmp_bytes_recv_per_msg_max  = [0 for x in unique_n_threads]
                tmp_bytes_recv_per_msg_avg  = [0 for x in unique_n_threads]
                tmp_throughput_recv_min     = [0 for x in unique_n_threads]
                tmp_throughput_recv_max     = [0 for x in unique_n_threads]
                tmp_throughput_recv_avg     = [0 for x in unique_n_threads]

                idx = 0
                for thr in unique_n_threads:
                    tmp_list_thr = [x for x in tmp_list if x.n_threads == thr]
                    # calculate mean values
                    tmp_time_chameleon[idx]         = st.mean([x.time_chameleon for x in tmp_list_thr])
                    tmp_time_original[idx]          = st.mean([x.time_openmp_only for x in tmp_list_thr])
                    tmp_n_tasks_local[idx]          = st.mean([x.n_local_tasks for x in tmp_list_thr])
                    tmp_n_tasks_remote[idx]         = st.mean([x.n_remote_tasks for x in tmp_list_thr])
                    
                    # tmp_bytes_send_per_msg_min[idx] = st.mean([x.bytes_send_per_msg_min for x in tmp_list_thr if x.sends_happened])
                    # tmp_bytes_send_per_msg_max[idx] = st.mean([x.bytes_send_per_msg_max for x in tmp_list_thr if x.sends_happened])
                    # tmp_bytes_send_per_msg_avg[idx] = st.mean([x.bytes_send_per_msg_avg for x in tmp_list_thr if x.sends_happened])
                    # tmp_throughput_send_min[idx]    = st.mean([x.throughput_send_min for x in tmp_list_thr if x.sends_happened])
                    # tmp_throughput_send_max[idx]    = st.mean([x.throughput_send_max for x in tmp_list_thr if x.sends_happened])
                    # tmp_throughput_send_avg[idx]    = st.mean([x.throughput_send_avg for x in tmp_list_thr if x.sends_happened])

                    # tmp_bytes_recv_per_msg_min[idx] = st.mean([x.bytes_recv_per_msg_min for x in tmp_list_thr if x.recvs_happened])
                    # tmp_bytes_recv_per_msg_max[idx] = st.mean([x.bytes_recv_per_msg_max for x in tmp_list_thr if x.recvs_happened])
                    # tmp_bytes_recv_per_msg_avg[idx] = st.mean([x.bytes_recv_per_msg_avg for x in tmp_list_thr if x.recvs_happened])
                    # tmp_throughput_recv_min[idx]    = st.mean([x.throughput_recv_min for x in tmp_list_thr if x.recvs_happened])
                    # tmp_throughput_recv_max[idx]    = st.mean([x.throughput_recv_max for x in tmp_list_thr if x.recvs_happened])
                    # tmp_throughput_recv_avg[idx]    = st.mean([x.throughput_recv_avg for x in tmp_list_thr if x.recvs_happened])

                    idx = idx + 1
                # append arrays
                arr_time_original.append(tmp_time_original)
                arr_time_chameleon.append(tmp_time_chameleon)
                arr_n_tasks_local.append(tmp_n_tasks_local)
                arr_n_tasks_remote.append(tmp_n_tasks_remote)

                arr_bytes_send_per_msg_min.append(tmp_bytes_send_per_msg_min)
                arr_bytes_send_per_msg_max.append(tmp_bytes_send_per_msg_max)
                arr_bytes_send_per_msg_avg.append(tmp_bytes_send_per_msg_avg)
                arr_throughput_send_min.append(tmp_throughput_send_min)
                arr_throughput_send_max.append(tmp_throughput_send_max)
                arr_throughput_send_avg.append(tmp_throughput_send_avg)

                arr_bytes_recv_per_msg_min.append(tmp_bytes_recv_per_msg_min)
                arr_bytes_recv_per_msg_max.append(tmp_bytes_recv_per_msg_max)
                arr_bytes_recv_per_msg_avg.append(tmp_bytes_recv_per_msg_avg)
                arr_throughput_recv_min.append(tmp_throughput_recv_min)
                arr_throughput_recv_max.append(tmp_throughput_recv_max)
                arr_throughput_recv_avg.append(tmp_throughput_recv_avg)

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
            
            # writer.writerow([])
            # writer.writerow(['Bytes_Send_Per_Msg_Min'] + unique_n_threads)
            # for tmp_idx in range(len(arr_types)):
            #     writer.writerow([arr_types[tmp_idx]] + arr_bytes_send_per_msg_min[tmp_idx])
            # writer.writerow([])
            # writer.writerow(['Bytes_Send_Per_Msg_Max'] + unique_n_threads)
            # for tmp_idx in range(len(arr_types)):
            #     writer.writerow([arr_types[tmp_idx]] + arr_bytes_send_per_msg_max[tmp_idx])
            # writer.writerow([])
            # writer.writerow(['Bytes_Send_Per_Msg_Avg'] + unique_n_threads)
            # for tmp_idx in range(len(arr_types)):
            #     writer.writerow([arr_types[tmp_idx]] + arr_bytes_send_per_msg_avg[tmp_idx])
            # writer.writerow([])
            # writer.writerow(['Throughput_Send_Min'] + unique_n_threads)
            # for tmp_idx in range(len(arr_types)):
            #     writer.writerow([arr_types[tmp_idx]] + arr_throughput_send_min[tmp_idx])
            # writer.writerow([])
            # writer.writerow(['Throughput_Send_Max'] + unique_n_threads)
            # for tmp_idx in range(len(arr_types)):
            #     writer.writerow([arr_types[tmp_idx]] + arr_throughput_send_max[tmp_idx])
            # writer.writerow([])
            # writer.writerow(['Throughput_Send_Avg'] + unique_n_threads)
            # for tmp_idx in range(len(arr_types)):
            #     writer.writerow([arr_types[tmp_idx]] + arr_throughput_send_avg[tmp_idx])

            # writer.writerow([])
            # writer.writerow(['Bytes_Recv_Per_Msg_Min'] + unique_n_threads)
            # for tmp_idx in range(len(arr_types)):
            #     writer.writerow([arr_types[tmp_idx]] + arr_bytes_recv_per_msg_min[tmp_idx])
            # writer.writerow([])
            # writer.writerow(['Bytes_Recv_Per_Msg_Max'] + unique_n_threads)
            # for tmp_idx in range(len(arr_types)):
            #     writer.writerow([arr_types[tmp_idx]] + arr_bytes_recv_per_msg_max[tmp_idx])
            # writer.writerow([])
            # writer.writerow(['Bytes_Recv_Per_Msg_Avg'] + unique_n_threads)
            # for tmp_idx in range(len(arr_types)):
            #     writer.writerow([arr_types[tmp_idx]] + arr_bytes_recv_per_msg_avg[tmp_idx])
            # writer.writerow([])
            # writer.writerow(['Throughput_Recv_Min'] + unique_n_threads)
            # for tmp_idx in range(len(arr_types)):
            #     writer.writerow([arr_types[tmp_idx]] + arr_throughput_recv_min[tmp_idx])
            # writer.writerow([])
            # writer.writerow(['Throughput_Recv_Max'] + unique_n_threads)
            # for tmp_idx in range(len(arr_types)):
            #     writer.writerow([arr_types[tmp_idx]] + arr_throughput_recv_max[tmp_idx])
            # writer.writerow([])
            # writer.writerow(['Throughput_Recv_Avg'] + unique_n_threads)
            # for tmp_idx in range(len(arr_types)):
            #     writer.writerow([arr_types[tmp_idx]] + arr_throughput_recv_avg[tmp_idx])

        # plot results
        tmp_target_file_name = "plot_granularity_" + str(int(gran))
        tmp_target_file_path = os.path.join(target_folder_plot, tmp_target_file_name)
        plotData(tmp_target_file_path, unique_n_threads, arr_types, arr_time_original, arr_time_chameleon, arr_n_tasks_remote, title_prefix + " - Granularity " + str(int(gran)), "# threads per rank")
        
        # plotDataMinMaxAvg(tmp_target_file_path + "_bytes_send", unique_n_threads, arr_types, arr_bytes_send_per_msg_min, arr_bytes_send_per_msg_max, arr_bytes_send_per_msg_avg, title_prefix + " - Granularity " + str(int(gran)) + " - Bytes Send", "# threads per rank", "Data Volume [KB]", True, divisor=1000)
        # plotDataMinMaxAvg(tmp_target_file_path + "_bytes_recv", unique_n_threads, arr_types, arr_bytes_recv_per_msg_min, arr_bytes_recv_per_msg_max, arr_bytes_recv_per_msg_avg, title_prefix + " - Granularity " + str(int(gran)) + " - Bytes Recv", "# threads per rank", "Data Volume [KB]", True, divisor=1000)
        # plotDataMinMaxAvg(tmp_target_file_path + "_throughput_send", unique_n_threads, arr_types, arr_throughput_send_min, arr_throughput_send_max, arr_throughput_send_avg, title_prefix + " - Granularity " + str(int(gran)) + " - Throughput Send", "# threads per rank", "Throughput [MB/s]")
        # plotDataMinMaxAvg(tmp_target_file_path + "_throughput_recv", unique_n_threads, arr_types, arr_throughput_recv_min, arr_throughput_recv_max, arr_throughput_recv_avg, title_prefix + " - Granularity " + str(int(gran)) + " - Throughput Recv", "# threads per rank", "Throughput [MB/s]")

    # ========== Generate results with fixed number of threads
    for thr in unique_n_threads:
        sub_list = [x for x in list_results if x.n_threads == thr]
        
        arr_types                   = []
        arr_time_original           = []
        arr_time_chameleon          = []
        arr_n_tasks_local           = []
        arr_n_tasks_remote          = []

        # used from first rank
        arr_bytes_send_per_msg_min  = []
        arr_bytes_send_per_msg_max  = []
        arr_bytes_send_per_msg_avg  = []
        arr_throughput_send_min     = []
        arr_throughput_send_max     = []
        arr_throughput_send_avg     = []

        # used from last rank
        arr_bytes_recv_per_msg_min  = []
        arr_bytes_recv_per_msg_max  = []
        arr_bytes_recv_per_msg_avg  = []
        arr_throughput_recv_min     = []
        arr_throughput_recv_max     = []
        arr_throughput_recv_avg     = []


        for ty in unique_types:
            tmp_list = [x for x in sub_list if x.result_type == ty]            
            if tmp_list:
                arr_types.append(ty)
                tmp_time_original   = [0 for x in unique_granularities]
                tmp_time_chameleon  = [0 for x in unique_granularities]
                tmp_n_tasks_local   = [0 for x in unique_granularities]
                tmp_n_tasks_remote  = [0 for x in unique_granularities]

                # used from first rank
                tmp_bytes_send_per_msg_min  = [0 for x in unique_granularities]
                tmp_bytes_send_per_msg_max  = [0 for x in unique_granularities]
                tmp_bytes_send_per_msg_avg  = [0 for x in unique_granularities]
                tmp_throughput_send_min     = [0 for x in unique_granularities]
                tmp_throughput_send_max     = [0 for x in unique_granularities]
                tmp_throughput_send_avg     = [0 for x in unique_granularities]

                # used from last rank
                tmp_bytes_recv_per_msg_min  = [0 for x in unique_granularities]
                tmp_bytes_recv_per_msg_max  = [0 for x in unique_granularities]
                tmp_bytes_recv_per_msg_avg  = [0 for x in unique_granularities]
                tmp_throughput_recv_min     = [0 for x in unique_granularities]
                tmp_throughput_recv_max     = [0 for x in unique_granularities]
                tmp_throughput_recv_avg     = [0 for x in unique_granularities]

                idx = 0
                for gran in unique_granularities:
                    tmp_list_thr = [x for x in tmp_list if x.task_granularity == gran]
                    # calculate mean values
                    tmp_time_chameleon[idx]         = st.mean([x.time_chameleon for x in tmp_list_thr])
                    tmp_time_original[idx]          = st.mean([x.time_openmp_only for x in tmp_list_thr])
                    tmp_n_tasks_local[idx]          = st.mean([x.n_local_tasks for x in tmp_list_thr])
                    tmp_n_tasks_remote[idx]         = st.mean([x.n_remote_tasks for x in tmp_list_thr])

                    # tmp_bytes_send_per_msg_min[idx] = st.mean([x.bytes_send_per_msg_min for x in tmp_list_thr if x.sends_happened])
                    # tmp_bytes_send_per_msg_max[idx] = st.mean([x.bytes_send_per_msg_max for x in tmp_list_thr if x.sends_happened])
                    # tmp_bytes_send_per_msg_avg[idx] = st.mean([x.bytes_send_per_msg_avg for x in tmp_list_thr if x.sends_happened])
                    # tmp_throughput_send_min[idx]    = st.mean([x.throughput_send_min for x in tmp_list_thr if x.sends_happened])
                    # tmp_throughput_send_max[idx]    = st.mean([x.throughput_send_max for x in tmp_list_thr if x.sends_happened])
                    # tmp_throughput_send_avg[idx]    = st.mean([x.throughput_send_avg for x in tmp_list_thr if x.sends_happened])

                    # tmp_bytes_recv_per_msg_min[idx] = st.mean([x.bytes_recv_per_msg_min for x in tmp_list_thr if x.recvs_happened])
                    # tmp_bytes_recv_per_msg_max[idx] = st.mean([x.bytes_recv_per_msg_max for x in tmp_list_thr if x.recvs_happened])
                    # tmp_bytes_recv_per_msg_avg[idx] = st.mean([x.bytes_recv_per_msg_avg for x in tmp_list_thr if x.recvs_happened])
                    # tmp_throughput_recv_min[idx]    = st.mean([x.throughput_recv_min for x in tmp_list_thr if x.recvs_happened])
                    # tmp_throughput_recv_max[idx]    = st.mean([x.throughput_recv_max for x in tmp_list_thr if x.recvs_happened])
                    # tmp_throughput_recv_avg[idx]    = st.mean([x.throughput_recv_avg for x in tmp_list_thr if x.recvs_happened])

                    idx = idx + 1
                # append arrays
                arr_time_original.append(tmp_time_original)
                arr_time_chameleon.append(tmp_time_chameleon)
                arr_n_tasks_local.append(tmp_n_tasks_local)
                arr_n_tasks_remote.append(tmp_n_tasks_remote)

                arr_bytes_send_per_msg_min.append(tmp_bytes_send_per_msg_min)
                arr_bytes_send_per_msg_max.append(tmp_bytes_send_per_msg_max)
                arr_bytes_send_per_msg_avg.append(tmp_bytes_send_per_msg_avg)
                arr_throughput_send_min.append(tmp_throughput_send_min)
                arr_throughput_send_max.append(tmp_throughput_send_max)
                arr_throughput_send_avg.append(tmp_throughput_send_avg)

                arr_bytes_recv_per_msg_min.append(tmp_bytes_recv_per_msg_min)
                arr_bytes_recv_per_msg_max.append(tmp_bytes_recv_per_msg_max)
                arr_bytes_recv_per_msg_avg.append(tmp_bytes_recv_per_msg_avg)
                arr_throughput_recv_min.append(tmp_throughput_recv_min)
                arr_throughput_recv_max.append(tmp_throughput_recv_max)
                arr_throughput_recv_avg.append(tmp_throughput_recv_avg)

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

            # writer.writerow([])
            # writer.writerow(['Bytes_Send_Per_Msg_Min'] + unique_granularities)
            # for tmp_idx in range(len(arr_types)):
            #     writer.writerow([arr_types[tmp_idx]] + arr_bytes_send_per_msg_min[tmp_idx])
            # writer.writerow([])
            # writer.writerow(['Bytes_Send_Per_Msg_Max'] + unique_granularities)
            # for tmp_idx in range(len(arr_types)):
            #     writer.writerow([arr_types[tmp_idx]] + arr_bytes_send_per_msg_max[tmp_idx])
            # writer.writerow([])
            # writer.writerow(['Bytes_Send_Per_Msg_Avg'] + unique_granularities)
            # for tmp_idx in range(len(arr_types)):
            #     writer.writerow([arr_types[tmp_idx]] + arr_bytes_send_per_msg_avg[tmp_idx])
            # writer.writerow([])
            # writer.writerow(['Throughput_Send_Min'] + unique_granularities)
            # for tmp_idx in range(len(arr_types)):
            #     writer.writerow([arr_types[tmp_idx]] + arr_throughput_send_min[tmp_idx])
            # writer.writerow([])
            # writer.writerow(['Throughput_Send_Max'] + unique_granularities)
            # for tmp_idx in range(len(arr_types)):
            #     writer.writerow([arr_types[tmp_idx]] + arr_throughput_send_max[tmp_idx])
            # writer.writerow([])
            # writer.writerow(['Throughput_Send_Avg'] + unique_granularities)
            # for tmp_idx in range(len(arr_types)):
            #     writer.writerow([arr_types[tmp_idx]] + arr_throughput_send_avg[tmp_idx])

            # writer.writerow([])
            # writer.writerow(['Bytes_Recv_Per_Msg_Min'] + unique_granularities)
            # for tmp_idx in range(len(arr_types)):
            #     writer.writerow([arr_types[tmp_idx]] + arr_bytes_recv_per_msg_min[tmp_idx])
            # writer.writerow([])
            # writer.writerow(['Bytes_Recv_Per_Msg_Max'] + unique_granularities)
            # for tmp_idx in range(len(arr_types)):
            #     writer.writerow([arr_types[tmp_idx]] + arr_bytes_recv_per_msg_max[tmp_idx])
            # writer.writerow([])
            # writer.writerow(['Bytes_Recv_Per_Msg_Avg'] + unique_granularities)
            # for tmp_idx in range(len(arr_types)):
            #     writer.writerow([arr_types[tmp_idx]] + arr_bytes_recv_per_msg_avg[tmp_idx])
            # writer.writerow([])
            # writer.writerow(['Throughput_Recv_Min'] + unique_granularities)
            # for tmp_idx in range(len(arr_types)):
            #     writer.writerow([arr_types[tmp_idx]] + arr_throughput_recv_min[tmp_idx])
            # writer.writerow([])
            # writer.writerow(['Throughput_Recv_Max'] + unique_granularities)
            # for tmp_idx in range(len(arr_types)):
            #     writer.writerow([arr_types[tmp_idx]] + arr_throughput_recv_max[tmp_idx])
            # writer.writerow([])
            # writer.writerow(['Throughput_Recv_Avg'] + unique_granularities)
            # for tmp_idx in range(len(arr_types)):
            #     writer.writerow([arr_types[tmp_idx]] + arr_throughput_recv_avg[tmp_idx])

        # plot results
        tmp_target_file_name = "plot_threads_" + str(int(thr))
        tmp_target_file_path = os.path.join(target_folder_plot, tmp_target_file_name)
        plotData(tmp_target_file_path, unique_granularities, arr_types, arr_time_original, arr_time_chameleon, arr_n_tasks_remote, title_prefix + " - " + str(int(thr)) + " Threads", "# task granularity (matrix size)")

        # plotDataMinMaxAvg(tmp_target_file_path + "_bytes_send", unique_granularities, arr_types, arr_bytes_send_per_msg_min, arr_bytes_send_per_msg_max, arr_bytes_send_per_msg_avg, title_prefix + " - " + str(int(thr)) + " Threads" + " - Bytes Send", "# task granularity (matrix size)", "Data Volume [KB]", True, divisor=1000)
        # plotDataMinMaxAvg(tmp_target_file_path + "_bytes_recv", unique_granularities, arr_types, arr_bytes_recv_per_msg_min, arr_bytes_recv_per_msg_max, arr_bytes_recv_per_msg_avg, title_prefix + " - " + str(int(thr)) + " Threads" + " - Bytes Recv", "# task granularity (matrix size)", "Data Volume [KB]", True, divisor=1000)
        # plotDataMinMaxAvg(tmp_target_file_path + "_throughput_send", unique_granularities, arr_types, arr_throughput_send_min, arr_throughput_send_max, arr_throughput_send_avg, title_prefix + " - " + str(int(thr)) + " Threads" + " - Throughput Send", "# task granularity (matrix size)", "Throughput [MB/s]")
        # plotDataMinMaxAvg(tmp_target_file_path + "_throughput_recv", unique_granularities, arr_types, arr_throughput_recv_min, arr_throughput_recv_max, arr_throughput_recv_avg, title_prefix + " - " + str(int(thr)) + " Threads" + " - Throughput Recv", "# task granularity (matrix size)", "Throughput [MB/s]")