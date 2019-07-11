import os, sys
import numpy as np
import statistics as st
from datetime import datetime
from CResult import *
import numpy as np
import matplotlib.pyplot as plt

# basic plot settings
F_SIZE = 16
plt.rc('font', size=F_SIZE)             # controls default text sizes
plt.rc('axes', titlesize=F_SIZE)        # fontsize of the axes title
plt.rc('axes', labelsize=F_SIZE)        # fontsize of the x and y labels
plt.rc('xtick', labelsize=F_SIZE)       # fontsize of the tick labels
plt.rc('ytick', labelsize=F_SIZE)       # fontsize of the tick labels
plt.rc('legend', fontsize=F_SIZE)       # legend fontsize
plt.rc('figure', titlesize=F_SIZE)      # fontsize of the figure title

def plotData(target_file_path, list_objects, arr_labels, text_header):
    xtick = list(range(len(list_objects[0].msg_size_kb)))
    tmp_colors = ['darkorange', 'green', 'red']

    # ========== Throughput
    path_result_img = target_file_path + "_throughput.png"
    fig = plt.figure(figsize=(16, 9),frameon=False)
    ax = fig.gca()
    # baseline first
    for idx_type in range(len(list_objects)):
        ax.plot(xtick, np.array(list_objects[idx_type].throughput_mb_s), 'x-', linewidth=2, color=tmp_colors[idx_type])
    plt.xticks(xtick, list_objects[0].msg_size_kb, rotation=45, ha='center')
    ax.minorticks_on()
    ax.legend(arr_labels, fancybox=True, shadow=False)                
    ax.grid(b=True, which='major', axis="both", linestyle='-', linewidth=1)
    ax.grid(b=True, which='minor', axis="both", linestyle='-', linewidth=0.4)
    ax.set_xlabel("Msg size [KB]")
    ax.set_ylabel("Throughput [MB/s]")
    ax.set_title(text_header + " - Throughput" )
    fig.savefig(path_result_img, dpi=None, facecolor='w', edgecolor='w', 
        format="png", transparent=False, bbox_inches='tight', pad_inches=0,
        frameon=False, metadata=None)
    plt.close(fig)

    # ========== L3 miss ratio
    path_result_img = target_file_path + "_l3miss.png"
    fig = plt.figure(figsize=(16, 9),frameon=False)
    ax = fig.gca()
    # baseline first
    for idx_type in range(len(list_objects)):
        ax.plot(xtick, np.array([x*100.0 for x in list_objects[idx_type].l3_miss_ratio]), 'x-', linewidth=2, color=tmp_colors[idx_type])
    plt.xticks(xtick, list_objects[0].msg_size_kb, rotation=45, ha='center')
    ax.minorticks_on()
    ax.legend(arr_labels, fancybox=True, shadow=False)                
    ax.grid(b=True, which='major', axis="both", linestyle='-', linewidth=1)
    ax.grid(b=True, which='minor', axis="both", linestyle='-', linewidth=0.4)
    ax.set_xlabel("Msg size [KB]")
    ax.set_ylabel("ratio [%]")
    ax.set_title(text_header + " - L3 miss ratio" )
    fig.savefig(path_result_img, dpi=None, facecolor='w', edgecolor='w', 
        format="png", transparent=False, bbox_inches='tight', pad_inches=0,
        frameon=False, metadata=None)
    plt.close(fig)

    # ========== L3 load miss ratio
    path_result_img = target_file_path + "_l3loadmiss.png"
    fig = plt.figure(figsize=(16, 9),frameon=False)
    ax = fig.gca()
    # baseline first
    for idx_type in range(len(list_objects)):
        ax.plot(xtick, np.array([x*100.0 for x in list_objects[idx_type].l3_load_miss_ratio]), 'x-', linewidth=2, color=tmp_colors[idx_type])
    plt.xticks(xtick, list_objects[0].msg_size_kb, rotation=45, ha='center')
    ax.minorticks_on()
    ax.legend(arr_labels, fancybox=True, shadow=False)                
    ax.grid(b=True, which='major', axis="both", linestyle='-', linewidth=1)
    ax.grid(b=True, which='minor', axis="both", linestyle='-', linewidth=0.4)
    ax.set_xlabel("Msg size [KB]")
    ax.set_ylabel("ratio [%]")
    ax.set_title(text_header + " - L3 load miss ratio" )
    fig.savefig(path_result_img, dpi=None, facecolor='w', edgecolor='w', 
        format="png", transparent=False, bbox_inches='tight', pad_inches=0,
        frameon=False, metadata=None)
    plt.close(fig)

    if "Distribution" in text_header:
        # ========== Instructions
        path_result_img = target_file_path + "_instructions.png"
        fig = plt.figure(figsize=(16, 9),frameon=False)
        ax = fig.gca()
        # baseline first
        for idx_type in range(len(list_objects)):
            if idx_type == 0:
                ax.plot(xtick, np.array([1 for x in list_objects[idx_type].total_instructions]), 'x-', linewidth=2, color=tmp_colors[idx_type])
            else:
                tmp_len     = len(list_objects[idx_type].total_instructions)
                tmp_ratio   = [list_objects[idx_type].total_instructions[x] / float(list_objects[0].total_instructions[x]) for x in range(tmp_len)]
                ax.plot(xtick, np.array(tmp_ratio), 'x-', linewidth=2, color=tmp_colors[idx_type])
        plt.xticks(xtick, list_objects[0].msg_size_kb, rotation=45, ha='center')
        ax.minorticks_on()
        ax.legend(arr_labels, fancybox=True, shadow=False)                
        ax.grid(b=True, which='major', axis="both", linestyle='-', linewidth=1)
        ax.grid(b=True, which='minor', axis="both", linestyle='-', linewidth=0.4)
        ax.set_xlabel("Msg size [KB]")
        ax.set_ylabel("Factor")
        ax.set_title(text_header + " - Instructions completed (compared to type0)" )
        fig.savefig(path_result_img, dpi=None, facecolor='w', edgecolor='w', 
            format="png", transparent=False, bbox_inches='tight', pad_inches=0,
            frameon=False, metadata=None)
        plt.close(fig)

if __name__ == "__main__":
    source_folder       = sys.argv[1]
    target_folder_plot  = os.path.join(source_folder, "result_plots")

    # create target directories of not yet existing
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
    unique_send_types = sorted(list(set([x.send_type for x in list_results])))
    # get unique number of threads
    unique_process_distribution = sorted(list(set([x.process_distribution for x in list_results])))

    # ========== Generate results for send types
    for cur_type in unique_send_types:
        sub_list = [x for x in list_results if x.send_type == cur_type]

        # create plots here
        tmp_target_file_name = "plot_sendtype_" + str(cur_type)
        tmp_target_file_path = os.path.join(target_folder_plot, tmp_target_file_name)
        arr_labels = [x.process_distribution for x in sub_list]
        plotData(tmp_target_file_path, sub_list, arr_labels, "Send Type " + str(cur_type))

    # ========== Generate results for process_distribution
    for cur_dist in unique_process_distribution:
        sub_list = [x for x in list_results if x.process_distribution == cur_dist]

        # create plots here
        tmp_target_file_name = "plot_distribution_" + str(cur_dist)
        tmp_target_file_path = os.path.join(target_folder_plot, tmp_target_file_name)
        arr_labels = [x.send_type for x in sub_list]
        plotData(tmp_target_file_path, sub_list, arr_labels, "Process Distribution " + str(cur_dist))