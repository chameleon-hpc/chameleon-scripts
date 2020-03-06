import os, sys
import numpy as np
import statistics as st
import matplotlib.pyplot as plt
import csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'common')))
from CChameleonStats import *
from CChameleonAggregation import *
from CChameleonPlotFunctions import *
from CChameleonCSVFunctions import *
from CCustomFileMetaData import *

if __name__ == "__main__":
    source_folder       = "C:\\J.Klinkenberg.Local\\repos\\chameleon\\chameleon-data\\2020-03-06_CommunicationModes\\20200306_122819_results\\2procs_dm"
    
    target_folder_data  = os.path.join(source_folder, "result_data")
    target_folder_plot  = os.path.join(source_folder, "result_plots")

    # create target directories of not yet existing
    if not os.path.exists(target_folder_data):
        os.makedirs(target_folder_data)
    if not os.path.exists(target_folder_plot):
        os.makedirs(target_folder_plot)

    # TODO: use the same names in output and data structure to ease specification
    list_signal_filter_read     = ["_num_executed_tasks_stolen", "_time_task_execution_stolen_sum"]
    list_signals                = ["execution_time", "speedup", "num_executed_tasks_stolen", "task_exec_stolen"]
    default_vals_group          = [None, 1.0, 0.0, 0.0]
    list_signals_labels         = ["Execution time", "Speedup", "Stolen tasks", "Execution time stolen tasks"]
    list_y_labels               = ["Time [sec]", "Speedup", "# stolen tasks", "Time [sec]"]
    list_y_limit                = [None, None, None, None]
    
    list_files = []
    # parse file names to be able to build groups later
    for file in os.listdir(source_folder):
        if file.endswith(".log"):
            cur_file_path = os.path.join(source_folder, file)
            print(cur_file_path)

            # read file and chameleon stats
            file_meta = CCustomFileMetaData(cur_file_path)
            cur_stats = CChameleonStatsPerRun()
            cur_stats.parseFile(cur_file_path, list_signal_filter_read)

            # add custom measurements to stats file that can be used later
            with open(cur_file_path) as f:
                # get exec time
                for line in f:
                    if "with chameleon took" in line or "with normal tasking took" in line:
                        tmp_split = line.split(" ")
                        cur_stats.execution_time = float(tmp_split[-1].strip())
                        break

            # save stats in base object
            file_meta.set_stats(cur_stats)
            list_files.append(file_meta)

    # calculate speedup
    for tmp_f in list_files:
        if tmp_f.is_baseline:
            tmp_f.stats.speedup = 1.0
        else:
            # find corresponding entries from baseline
            tmp_l_bs = [x for x in list_files if 
                x.is_baseline and 
                x.is_distributed_memory == tmp_f.is_distributed_memory and 
                x.task_granularity == tmp_f.task_granularity and 
                x.nr_ranks == tmp_f.nr_ranks]
            # get mean time for baseline as reference
            cur_data_list = aggregate_chameleon_statistics( [x.stats for x in tmp_l_bs], 
                                                            ["execution_time"], 
                                                            aggregation_metric=EnumAggregationMetric.SUM,
                                                            aggregation_for_run=EnumAggregationTypeRun.SUM,
                                                            aggegration_for_group=EnumAggregationTypeGroup.AVG)
            tmp_f.stats.speedup = cur_data_list[0] / tmp_f.stats.execution_time
    
    # get unique types
    unique_types = sorted(list(set([x.type for x in list_files])))
    # get unique number of threads
    unique_granularities = sorted(list(set([x.task_granularity for x in list_files])))

    arr_data_plot           = [[] for x in list_signals]
    arr_types               = []
    tmp_stat_objs_per_type  = []
    
    for ty in unique_types:
        tmp_list = [x for x in list_files if x.type == ty]
        if tmp_list:
            arr_types.append(ty + " - " + str(tmp_list[0].nr_threads) + "t")
            tmp_stat_objs_per_type.append([x for x in tmp_list])
            tmp_data_plot = [[] for x in list_signals]

            for gran in unique_granularities:
                sub_list    = [x for x in tmp_list if x.task_granularity == gran]
                cur_data_list = aggregate_chameleon_statistics( [x.stats for x in sub_list], 
                                                            list_signals, 
                                                            aggregation_metric=EnumAggregationMetric.SUM,
                                                            aggregation_for_run=EnumAggregationTypeRun.SUM,
                                                            aggegration_for_group=EnumAggregationTypeGroup.AVG,
                                                            default_vals_group=default_vals_group)
                for idx_sig in range(len(cur_data_list)):
                    tmp_data_plot[idx_sig].append(cur_data_list[idx_sig])

            for idx_sig in range(len(tmp_data_plot)):
                arr_data_plot[idx_sig].append(tmp_data_plot[idx_sig])    

    # plot signals
    for idx_sig in range(len(list_signals)):
        tmp_target_file_name = "plot_" + list_signals[idx_sig] + ".png"
        tmp_target_file_path = os.path.join(target_folder_plot, tmp_target_file_name)
        plot_data_normal(tmp_target_file_path, unique_granularities, arr_types, arr_data_plot[idx_sig], list_signals_labels[idx_sig], "# task granularity (matrix size)", list_y_labels[idx_sig], enforced_y_limit=list_y_limit[idx_sig])

    # csv output
    tmp_target_file_name = "output.result"
    tmp_target_file_path = os.path.join(target_folder_data, tmp_target_file_name)
    write_stats_data_mean(tmp_target_file_path, arr_types, tmp_stat_objs_per_type, list_signals, "task_granularity", unique_granularities)