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
    # source_folder       = "C:\\J.Klinkenberg.Local\\repos\\chameleon\\chameleon-data\\2019-10-31_JPDC_task_granularity_tests\\20191029_201619_results\\2procs_dm\\Test"
    #source_folder       = "/dss/dsshome1/02/di57zoh3/chameleon/chameleon-scripts/tests_mxm_replication/20200224_150956_results/2procs_rep_4"
    source_folder       = "/dss/dsshome1/02/di57zoh3/chameleon/chameleon-scripts/tests_mxm_replication/20200229_152918_results_100_4/2procs_rep_4"
    #source_folder       = "/dss/dsshome1/02/di57zoh3/chameleon/chameleon-scripts/tests_mxm_replication/20200228_133013_results_1000_4/2procs_rep_4"
    
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
    list_signals_labels         = ["Execution time", "Speedup", "Stolen tasks", "Execution time stolen tasks"]
    list_y_labels               = ["Time [sec]", "Speedup", "# stolen tasks", "Time [sec]"]
    list_y_limit                = [0, None, 0, 0]
    
    list_files = []
    # parse file names to be able to build groups later
    for file in os.listdir(source_folder):
        if file.endswith(".log")  and not("300") in file:
            cur_file_path = os.path.join(source_folder, file)
            print(cur_file_path)

            # read file and chameleon stats
            file_meta = CCustomFileMetaData(cur_file_path)
            cur_stats = CChameleonStatsPerRun()
            print (cur_file_path)
            cur_stats.parseFile(cur_file_path, list_signal_filter_read)

            # add custom measurements to stats file that can be used later
            with open(cur_file_path) as f:
                # get exec time
                for line in f:
                    if "with chameleon took" in line:
                        tmp_split = line.split(" ")
                        cur_stats.execution_time = float(tmp_split[-1].strip())
                        break
                for line in f:
                    if "with normal tasking took" in line:
                        tmp_split = line.split(" ")
                        cur_stats.time_openmp = float(tmp_split[-1].strip())
                        break

            # calculate speedup + add to stats struct
            cur_stats.speedup = cur_stats.time_openmp / cur_stats.execution_time

            # save stats in base object
            file_meta.set_stats(cur_stats)
            list_files.append(file_meta)
    
    # get unique types
    unique_types = sorted(list(set([x.percentage for x in list_files])))
    # get unique number of threads
    unique_n_threads = sorted(list(set([x.nr_threads for x in list_files])))
    # get unique number of threads
    unique_granularities = sorted(list(set([x.task_granularity for x in list_files])))

    for gran in unique_granularities:
        sub_list    = [x for x in list_files if x.task_granularity == gran]
        
        arr_types               = []
        arr_data_plot           = [[] for x in list_signals]        
        tmp_stat_objs_per_type  = []

        for ty in unique_types:
            tmp_list = [x for x in sub_list if x.percentage == ty]
            if tmp_list:
                arr_types.append(ty)
                tmp_stat_objs_per_type.append([x for x in tmp_list])
                tmp_data_plot       = [[] for x in list_signals]

                for thr in unique_n_threads:
                    sub_sub_list = [x for x in tmp_list if x.nr_threads == thr]
                    cur_data_list = aggregate_chameleon_statistics( [x.stats for x in sub_sub_list], 
                                                            list_signals, 
                                                            aggregation_metric=EnumAggregationMetric.SUM,
                                                            aggregation_for_run=EnumAggregationTypeRun.SUM,
                                                            aggegration_for_group=EnumAggregationTypeGroup.AVG)

                    for idx_res in range(len(cur_data_list)):
                        tmp_data_plot[idx_res].append(cur_data_list[idx_res])
                
                for idx_sig in range(len(list_signals)):
                    arr_data_plot[idx_sig].append(tmp_data_plot[idx_sig])

        # plot signals
        for idx_sig in range(len(list_signals)):
            tmp_target_file_name = "plot_granularity_" + str(int(gran)) + "_" + list_signals[idx_sig] + ".png"
            tmp_target_file_path = os.path.join(target_folder_plot, tmp_target_file_name)
            plot_data_normal(tmp_target_file_path, unique_n_threads, arr_types, arr_data_plot[idx_sig], "Granularity " + str(int(gran)) + " - " + list_signals_labels[idx_sig], "# threads per rank", list_y_labels[idx_sig], enforced_y_limit=list_y_limit[idx_sig])

        # csv output
        tmp_target_file_name = "output_granularity_" + str(gran) + ".result"
        tmp_target_file_path = os.path.join(target_folder_data, tmp_target_file_name)
        write_stats_data_mean(tmp_target_file_path, arr_types, tmp_stat_objs_per_type, list_signals, "nr_threads", unique_n_threads)

    for thr in unique_n_threads:   
        sub_list = [x for x in list_files if x.nr_threads == thr]
        arr_types               = []
        arr_data_plot           = [[] for x in list_signals]        
        tmp_stat_objs_per_type  = []

        for ty in unique_types:
            tmp_list = [x for x in sub_list if x.percentage == ty]
            if tmp_list:
                arr_types.append(ty)
                tmp_stat_objs_per_type.append([x for x in tmp_list])
                tmp_data_plot       = [[] for x in list_signals]

                for gran in unique_granularities:
                    sub_sub_list    = [x for x in tmp_list if x.task_granularity == gran]
                    cur_data_list = aggregate_chameleon_statistics( [x.stats for x in sub_sub_list], 
                                                            list_signals, 
                                                            aggregation_metric=EnumAggregationMetric.SUM,
                                                            aggregation_for_run=EnumAggregationTypeRun.SUM,
                                                            aggegration_for_group=EnumAggregationTypeGroup.AVG)

                    for idx_res in range(len(cur_data_list)):
                        tmp_data_plot[idx_res].append(cur_data_list[idx_res])
                
                for idx_sig in range(len(list_signals)):
                    arr_data_plot[idx_sig].append(tmp_data_plot[idx_sig])

        # plot signals
        for idx_sig in range(len(list_signals)):
            tmp_target_file_name = "plot_threads_" + str(int(thr)) + "_" + list_signals[idx_sig] + ".png"
            tmp_target_file_path = os.path.join(target_folder_plot, tmp_target_file_name)
            plot_data_normal(tmp_target_file_path, unique_granularities, arr_types, arr_data_plot[idx_sig], "Threads: " + str(int(thr)) + " - " + list_signals_labels[idx_sig], "# task granularity (matrix size)", list_y_labels[idx_sig], enforced_y_limit=list_y_limit[idx_sig])

        # csv output
        tmp_target_file_name = "output_threads_" + str(thr) + ".result"
        tmp_target_file_path = os.path.join(target_folder_data, tmp_target_file_name)
        write_stats_data_mean(tmp_target_file_path, arr_types, tmp_stat_objs_per_type, list_signals, "task_granularity", unique_granularities)

    # Detailed output per gran & nr_threads
    tmp_target_file_name = "output_detailed.result"
    tmp_target_file_path = os.path.join(target_folder_data, tmp_target_file_name)
    with open(tmp_target_file_path, mode='w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        for gran in unique_granularities:
            for thr in unique_n_threads:
                sub_list = [x for x in list_files if x.nr_threads == thr and x.task_granularity == gran]
                writer.writerow(['===== Details (avg) for granularity ' + str(gran) + ' - and thread ' + str(thr) + " ====="])
                for sig in list_signals:
                    writer.writerow([str(sig)])
                    for cur_type in arr_types:
                        cur_list_stats  = [x.stats for x in sub_list if x.percentage == cur_type]
                        tmp_vals        = aggregate_chameleon_statistics(cur_list_stats, [sig], aggegration_for_group=EnumAggregationTypeGroup.ALL)
                        tmp_vals        = tmp_vals[0] # only need first return value here
                        writer.writerow([cur_type] + tmp_vals)
                    writer.writerow([])
                writer.writerow([])
