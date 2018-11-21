#!/usr/bin/python3.6

import os, sys
import subprocess
import numpy as np
import matplotlib.pyplot as plt

class CPlotPackingTypeThresholds:
    def __init__(self, *args, **kwargs):
        pass

    def plotResults(self, dest_dir, suffixes, signals_to_plot, result_prefix=None):
        # read file content first from result files
        arr_file_content = []

        # contains the sizes retreived from first result file
        arr_sizes = []

        # will contain the data for plotting (2D: signals x suffixes)
        arr_data_plotting = []
        for i in range(len(signals_to_plot)):
            arr_data_plotting.append([])

        for name_suffix in suffixes:
            tmp_res_file_name   = "result_analysis_packing_type_" + name_suffix + ".txt"
            tmp_res_file_path   = os.path.join(dest_dir, tmp_res_file_name)

            tmp_arr = []
            with open(tmp_res_file_path) as file:
                for line in file:
                    tmp_arr.append(line)
            
            # append array with file contents
            arr_file_content.append(tmp_arr)

        # extract sizes
        tmp_contents = arr_file_content[0]
        for line in tmp_contents:
            if line.startswith("Sizes;"):
                tmp_spl = line.split(";")
                for idx_size in range(1, len(tmp_spl)-1):
                    # tmp_spl2 = tmp_spl[idx_size].split("x")
                    # cur_size = int(tmp_spl2[0])
                    # arr_sizes.append(cur_size)
                    arr_sizes.append(tmp_spl[idx_size])
                break
        
        # extract and parse data
        for fc in arr_file_content:
            for idx_signal in range(len(signals_to_plot)):
                tmp_signal = signals_to_plot[idx_signal]

                tmp_arr_data_all_versions = []
                for line in fc:
                    if(line.startswith(tmp_signal + ";")):
                        tmp_spl = line.split(";")
                        for idx_size in range(1, len(tmp_spl)-1):
                            cur_val = float(tmp_spl[idx_size])
                            tmp_arr_data_all_versions.append(cur_val)
                        break
                # set values for signal and suffix
                arr_data_plotting[idx_signal].append(tmp_arr_data_all_versions)
        
        # plot data
        xtick = list(range(len(arr_sizes)))

        for idx_signal in range(len(signals_to_plot)):
                tmp_signal = signals_to_plot[idx_signal]
                signal_shorter = tmp_signal[4:]
                fig = plt.figure(figsize=(16, 9))
                # only for debugging
                # plt.show()
                ax = fig.gca()
                labels = []
                for idx_suffix in range(len(suffixes)):
                    tmp_suffix  = suffixes[idx_suffix]
                    tmp_data    = arr_data_plotting[idx_signal][idx_suffix]
                    # ax.plot(xtick[:7], np.array(tmp_data[:7]), 'x-')
                    ax.plot(xtick, np.array(tmp_data), 'x-')
                    labels.append(tmp_suffix)
                
                plt.xticks(xtick, arr_sizes)
                ax.minorticks_on()
                ax.legend(labels, fancybox=True, shadow=False)                
                ax.grid(b=True, which='major', axis="both", linestyle='-', linewidth=1)
                ax.grid(b=True, which='minor', axis="both", linestyle='-', linewidth=0.4)
                ax.set_xlabel("Matrix Size")
                ax.set_ylabel("Time [sec]")
                
                if result_prefix is None:
                    ax.set_title("Results for   \"" + signal_shorter + "\"")
                    path_result_img = os.path.join(dest_dir, "Comparison_" + signal_shorter + ".png")
                else:
                    ax.set_title("Results for   \"" + signal_shorter + "\"   in   " + result_prefix)
                    path_result_img = os.path.join(dest_dir, "Comparison_" + result_prefix + "_" + signal_shorter + ".png")

                fig.savefig(path_result_img, dpi=None, facecolor='w', edgecolor='w', 
                    format="png", transparent=False, bbox_inches=None, pad_inches=0.1,
                    frameon=None, metadata=None)
                plt.close(fig)


# define directories
script_dir              = os.path.dirname(os.path.abspath(__file__))
application_dir         = os.path.join(script_dir, '..', '..', 'examples', 'matrix_example')
cur_working_dir         = os.getcwd()

# ======================= Start of Main Here =========================
if __name__ == "__main__":
    dest_dir = script_dir

    # define versions to be considered
    suffixes = []
    # suffixes.append("shared_buffer")
    # suffixes.append("shared_zero-copy")
    suffixes.append("distributed_buffer")
    suffixes.append("distributed_zero-copy")

    # define signals to be plotted
    signals = []
    signals.append("arr_encode_avg")
    signals.append("arr_decode_avg")
    signals.append("arr_offload_send_task_avg")
    signals.append("arr_offload_recv_task_avg")
    signals.append("arr_comb_send_task_avg")
    signals.append("arr_comb_recv_task_avg")

    # init plot object
    plot_obj = CPlotPackingTypeThresholds()
    # parse and plot
    # plot_obj.plotResults(dest_dir, suffixes, signals, "shared-mem")
    plot_obj.plotResults(dest_dir, suffixes, signals, "distributed-mem")
