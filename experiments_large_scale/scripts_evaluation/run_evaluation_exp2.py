import os, sys
import numpy as np
import statistics as st
import matplotlib.pyplot as plt
import csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'common')))
from CChameleonStats import *
from CChameleonAggregation import *
from CChameleonPlotFunctions import *
from CChameleonCSVFunctions import *
from CCustomFileMetaData_Exp2 import *
from CUtilProcessing import *

if __name__ == "__main__":
    source_folder       = "F:\\repos\\chameleon\\chameleon-data\\Test_results_experiment2"
    
    target_folder_data  = os.path.join(source_folder, "result_data")
    target_folder_plot  = os.path.join(source_folder, "result_plots")

    # create target directories of not yet existing
    if not os.path.exists(target_folder_data):
        os.makedirs(target_folder_data)
    if not os.path.exists(target_folder_plot):
        os.makedirs(target_folder_plot)

    # TODO: use the same names in output and data structure to ease specification
    # list_signal_filter_read     = ["_num_executed_tasks_stolen", "_time_task_execution_stolen_sum"]
    list_signal_filter_read     = []

    list_signals                = ["execution_time", "consumption_wh_overall", "consumption_wh_switches", "consumption_perc_switches", "power_draw_overall"]
    default_vals_group          = [None, 0.0, 0.0, 0.0, 0.0]
    list_signals_labels         = ["Execution time", "Energy Consumption - Overall", "Energy Consumption - Switches", "Energy Consumption - Percent Switches", "Mean Power Draw -  Overall"]
    list_y_labels               = ["Time [sec]", "Energy Consumption [Wh]", "Energy Consumption [Wh]", "Share [%]", "Power Draw [W]"]
    list_y_limit                = [None, None, None, None, None]
    
    list_files = []
    # parse file names to be able to build groups later
    for file in os.listdir(source_folder):
        if file.endswith(".log") and not file.endswith("power.log"):
            cur_file_path = os.path.join(source_folder, file)
            print(cur_file_path)

            # read file and chameleon stats
            file_meta = CCustomFileMetaData_Exp2(cur_file_path)
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
            
            # load power measurement values
            CUtilProcessing.parse_power_measurement(cur_file_path, cur_stats)
            CUtilProcessing.postprocess(cur_stats)

            # save stats in base object
            file_meta.set_stats(cur_stats)
            list_files.append(file_meta)
    
    # get unique values
    unique_types            = sorted(list(set([x.type for x in list_files])))
    unique_nr_nodes         = sorted(list(set([x.nr_nodes for x in list_files])))
    unique_nr_slow_nodes    = sorted(list(set([x.nr_slow_nodes for x in list_files])))
    unique_freq_slow        = sorted(list(set([x.freq_slow for x in list_files])))

    for nn in unique_nr_nodes:
        cur_list0 = [x for x in list_files if x.nr_nodes == nn]

        for freq in unique_freq_slow:
            cur_list = [x for x in cur_list0 if x.freq_slow == freq]

            arr_data_plot           = [[] for x in list_signals]
            arr_types               = []
            tmp_stat_objs_per_type  = []
            
            for ty in unique_types:
                tmp_list = [x for x in cur_list if x.type == ty]
                if tmp_list:
                    arr_types.append(ty + " - " + str(tmp_list[0].nr_threads) + "t")
                    tmp_stat_objs_per_type.append([x for x in tmp_list])
                    tmp_data_plot = [[] for x in list_signals]

                    for ns in unique_nr_slow_nodes:
                        sub_list    = [x for x in tmp_list if x.nr_slow_nodes == ns]
                        if sub_list:
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
                tmp_target_file_name = "plot_nodes_" + str(nn) + "_" + "freq_" + str(freq) + "_" + list_signals[idx_sig] + ".png"
                tmp_target_file_path = os.path.join(target_folder_plot, tmp_target_file_name)
                plot_data_normal(tmp_target_file_path, unique_nr_slow_nodes[0:len(arr_data_plot[idx_sig][0])], arr_types, arr_data_plot[idx_sig], list_signals_labels[idx_sig] + " - " + str(nn) + " Nodes (Slow Freq: " + str(freq / 1e6) + " GHz)", "# slow nodes", list_y_labels[idx_sig], enforced_y_limit=list_y_limit[idx_sig])

        for ns in unique_nr_slow_nodes:
            cur_list = [x for x in cur_list0 if x.nr_slow_nodes == ns]

            arr_data_plot           = [[] for x in list_signals]
            arr_types               = []
            tmp_stat_objs_per_type  = []
            
            for ty in unique_types:
                tmp_list = [x for x in cur_list if x.type == ty]
                if tmp_list:
                    arr_types.append(ty + " - " + str(tmp_list[0].nr_threads) + "t")
                    tmp_stat_objs_per_type.append([x for x in tmp_list])
                    tmp_data_plot = [[] for x in list_signals]

                    for freq in unique_freq_slow:
                        sub_list    = [x for x in tmp_list if x.freq_slow == freq]
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
                tmp_target_file_name = "plot_nodes_" + str(nn) + "_" + "nrslow_" + str(ns) + "_" + list_signals[idx_sig] + ".png"
                tmp_target_file_path = os.path.join(target_folder_plot, tmp_target_file_name)
                plot_data_normal(tmp_target_file_path, [x/1e6 for x in unique_freq_slow], arr_types, arr_data_plot[idx_sig], list_signals_labels[idx_sig] + " - " + str(nn) + " Nodes (Nr Slow Nodes: " + str(ns) + ")", "Freq. of slow nodes [GHz]", list_y_labels[idx_sig], enforced_y_limit=list_y_limit[idx_sig])

