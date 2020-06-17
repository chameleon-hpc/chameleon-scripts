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
    if len(sys.argv) < 2:
        print("Error: Not enough arguments.")
        print("Usage: python .\\run_evaluation_exp1 <folder_path_output_files>")
        exit(1)
    source_folder = sys.argv[1]
    if not os.path.exists(source_folder):
        print("Error: Folder path " + source_folder + " does not exist")
        exit(2)

    # source_folder = "F:\\repos\\chameleon\\chameleon-scripts\\tests_cholesky_compare_versions\\20200429_105804_results\\2procs_dm"
    
    target_folder_data  = os.path.join(source_folder, "result_data")
    target_folder_plot  = os.path.join(source_folder, "result_plots")

    # create target directories of not yet existing
    if not os.path.exists(target_folder_data):
        os.makedirs(target_folder_data)
    if not os.path.exists(target_folder_plot):
        os.makedirs(target_folder_plot)

    # # TODO: use the same names in output and data structure to ease specification
    # list_signal_filter_read     = ["_num_executed_tasks_stolen", "_time_task_execution_stolen_sum"]
    list_signals                = ["time_potrf", "time_trsm", "time_gemm", "time_syrk", "time_comm", "time_create", "execution_time", "gflops"]
    list_signals_labels         = ["Mean time for potrf", "Mean time for trsm", "Mean time for gemm", "Mean time for syrk", "Mean communication time", "Mean task creation time", "Execution time", "GFlops/s"]
    # default_vals_group          = [None, 1.0, 0.0, 0.0]
    list_y_labels               = ["Time [sec]", "Time [sec]", "Time [sec]", "Time [sec]", "Time [sec]", "Time [sec]", "Time [sec]", "GFlops/s"]
    list_y_limit                = [0, 0, 0, 0, 0, 0, 0, 0]
    
    list_files = []
    # parse file names to be able to build groups later
    for file in os.listdir(source_folder):
        if file.endswith(".log"):
            cur_file_path = os.path.join(source_folder, file)
            print(cur_file_path)

            # read file and chameleon stats
            file_meta = CCustomFileMetaData(cur_file_path)
            cur_stats = CChameleonStatsPerRun()
            cur_stats.parseFile(cur_file_path, None)
            cur_stats.stats_per_rank = [CChameleonStatsPerRank(i) for i in range(file_meta.nr_ranks)]

            for i in range(file_meta.nr_ranks):
                cur_stats.stats_per_rank[i].time_potrf  = CStatsDataPoint()
                cur_stats.stats_per_rank[i].time_gemm   = CStatsDataPoint()
                cur_stats.stats_per_rank[i].time_syrk   = CStatsDataPoint()
                cur_stats.stats_per_rank[i].time_trsm   = CStatsDataPoint()
                cur_stats.stats_per_rank[i].time_comm   = CStatsDataPoint()
                cur_stats.stats_per_rank[i].time_create = CStatsDataPoint()

            # add custom measurements to stats file that can be used later
            with open(cur_file_path) as f:
                # get exec time
                for line in f:
                    line = line.strip()
                    if line.startswith("test:"):
                        tmp_spl = line.split(":")
                        cur_stats.gflops = float(tmp_spl[11])
                        cur_stats.execution_time = float(tmp_spl[13])
                    elif line.startswith("["):
                        tmp_spl = line.split(" ")
                        if tmp_spl[1].strip().startswith("potrf"):
                            # get rank number
                            cur_rank = int(tmp_spl[0][1:-1])
                            spl2 = tmp_spl[1].split(":")
                            cur_stats.stats_per_rank[cur_rank].time_potrf.data_sum      = float(spl2[1])
                            cur_stats.stats_per_rank[cur_rank].time_trsm.data_sum       = float(spl2[3])
                            cur_stats.stats_per_rank[cur_rank].time_gemm.data_sum       = float(spl2[5])
                            cur_stats.stats_per_rank[cur_rank].time_syrk.data_sum       = float(spl2[7])
                            cur_stats.stats_per_rank[cur_rank].time_comm.data_sum       = float(spl2[9])
                            cur_stats.stats_per_rank[cur_rank].time_create.data_sum     = float(spl2[11])
                        elif tmp_spl[1].strip().startswith("count"):
                            # get rank number
                            cur_rank = int(tmp_spl[0][1:-1])
                            spl2 = tmp_spl[1].split(":")
                            cur_stats.stats_per_rank[cur_rank].time_potrf.data_count    = float(spl2[1])
                            cur_stats.stats_per_rank[cur_rank].time_trsm.data_count     = float(spl2[3])
                            cur_stats.stats_per_rank[cur_rank].time_gemm.data_count     = float(spl2[5])
                            cur_stats.stats_per_rank[cur_rank].time_syrk.data_count     = float(spl2[7])
                            cur_stats.stats_per_rank[cur_rank].time_comm.data_count     = 1
                            cur_stats.stats_per_rank[cur_rank].time_create.data_count   = 1

                            if cur_stats.stats_per_rank[cur_rank].time_potrf.data_count > 0:
                                cur_stats.stats_per_rank[cur_rank].time_potrf.data_avg      = cur_stats.stats_per_rank[cur_rank].time_potrf.data_sum / cur_stats.stats_per_rank[cur_rank].time_potrf.data_count
                            if cur_stats.stats_per_rank[cur_rank].time_trsm.data_count > 0:
                                cur_stats.stats_per_rank[cur_rank].time_trsm.data_avg       = cur_stats.stats_per_rank[cur_rank].time_trsm.data_sum / cur_stats.stats_per_rank[cur_rank].time_trsm.data_count
                            if cur_stats.stats_per_rank[cur_rank].time_gemm.data_count > 0:
                                cur_stats.stats_per_rank[cur_rank].time_gemm.data_avg       = cur_stats.stats_per_rank[cur_rank].time_gemm.data_sum / cur_stats.stats_per_rank[cur_rank].time_gemm.data_count
                            if cur_stats.stats_per_rank[cur_rank].time_syrk.data_count > 0:
                                cur_stats.stats_per_rank[cur_rank].time_syrk.data_avg       = cur_stats.stats_per_rank[cur_rank].time_syrk.data_sum / cur_stats.stats_per_rank[cur_rank].time_syrk.data_count
                            cur_stats.stats_per_rank[cur_rank].time_comm.data_avg       = cur_stats.stats_per_rank[cur_rank].time_comm.data_sum
                            cur_stats.stats_per_rank[cur_rank].time_create.data_avg     = cur_stats.stats_per_rank[cur_rank].time_create.data_sum

            # save stats in base object
            file_meta.set_stats(cur_stats)
            list_files.append(file_meta)
    
    # get unique stuff
    unique_categories   = sorted(list(set([x.category for x in list_files])))
    unique_versions     = sorted(list(set([x.version for x in list_files])))
    unique_mat_sizes    = sorted(list(set([x.matrix_size for x in list_files])))
    unique_block_sizes  = sorted(list(set([x.block_size for x in list_files])))

    for cat in unique_categories:
        tmp_list1 = [x for x in list_files if x.category == cat]

        # ============= Evaluate for fixed block size =============
        for b_size in unique_block_sizes:
            tmp_list2 = [x for x in tmp_list1 if x.block_size == b_size]
            arr_data_plot           = [[] for x in list_signals]
            arr_types               = []
            tmp_stat_objs_per_type  = []
        
            for ver in unique_versions:
                cur_list = [x for x in tmp_list2 if x.version == ver]
                if cur_list:
                    arr_types.append(ver + " (" + str(cur_list[0].nr_threads) + "t"+ ")")
                    tmp_stat_objs_per_type.append([x for x in cur_list])
                    tmp_data_plot = [[] for x in list_signals]

                    for m_size in unique_mat_sizes:
                        cur_list2 = [x for x in cur_list if x.matrix_size == m_size]
                        cur_data_list = aggregate_chameleon_statistics( [x.stats for x in cur_list2], 
                                            list_signals, 
                                            aggregation_metric=EnumAggregationMetric.AVG,
                                            aggregation_for_run=EnumAggregationTypeRun.AVG,
                                            aggegration_for_group=EnumAggregationTypeGroup.AVG)

                        for idx_sig in range(len(cur_data_list)):
                            tmp_data_plot[idx_sig].append(cur_data_list[idx_sig])

                    for idx_sig in range(len(tmp_data_plot)):
                        arr_data_plot[idx_sig].append(tmp_data_plot[idx_sig])

            # plot signals
            for idx_sig in range(len(list_signals)):
                tmp_target_file_name = "plot_bszie_" + str(b_size) + "_" + list_signals[idx_sig] + ".png"
                tmp_target_file_path = os.path.join(target_folder_plot, tmp_target_file_name)
                plot_data_normal(tmp_target_file_path, unique_mat_sizes, arr_types, arr_data_plot[idx_sig], "Block-Size(" + str(b_size) + ") R" + str(tmp_list2[0].nr_ranks) + "T" + str(tmp_list2[0].nr_threads) + " - " + list_signals_labels[idx_sig], "# task granularity (matrix size)", list_y_labels[idx_sig], enforced_y_limit=list_y_limit[idx_sig])

            # csv output
            tmp_target_file_name = "output_bsize_" + str(b_size) + ".txt"
            tmp_target_file_path = os.path.join(target_folder_data, tmp_target_file_name)
            write_stats_data_mean(tmp_target_file_path, arr_types, tmp_stat_objs_per_type, list_signals, "matrix_size", unique_mat_sizes)

        # ============= Evaluate for fixed matrix size =============
        for m_size in unique_mat_sizes:
            tmp_list2 = [x for x in tmp_list1 if x.matrix_size == m_size]
            arr_data_plot           = [[] for x in list_signals]
            arr_types               = []
            tmp_stat_objs_per_type  = []
        
            for ver in unique_versions:
                cur_list = [x for x in tmp_list2 if x.version == ver]
                if cur_list:
                    arr_types.append(ver + " (" + str(cur_list[0].nr_threads) + "t"+ ")")
                    tmp_stat_objs_per_type.append([x for x in cur_list])
                    tmp_data_plot = [[] for x in list_signals]

                    for b_size in unique_block_sizes:
                        cur_list2 = [x for x in cur_list if x.block_size == b_size]
                        cur_data_list = aggregate_chameleon_statistics( [x.stats for x in cur_list2], 
                                            list_signals, 
                                            aggregation_metric=EnumAggregationMetric.AVG,
                                            aggregation_for_run=EnumAggregationTypeRun.AVG,
                                            aggegration_for_group=EnumAggregationTypeGroup.AVG)

                        for idx_sig in range(len(cur_data_list)):
                            tmp_data_plot[idx_sig].append(cur_data_list[idx_sig])

                    for idx_sig in range(len(tmp_data_plot)):
                        arr_data_plot[idx_sig].append(tmp_data_plot[idx_sig])

            # plot signals
            for idx_sig in range(len(list_signals)):
                tmp_target_file_name = "plot_mszie_" + str(m_size) + "_" + list_signals[idx_sig] + ".png"
                tmp_target_file_path = os.path.join(target_folder_plot, tmp_target_file_name)
                plot_data_normal(tmp_target_file_path, unique_block_sizes, arr_types, arr_data_plot[idx_sig], "Matrix-Size(" + str(m_size) + ") R" + str(tmp_list2[0].nr_ranks) + "T" + str(tmp_list2[0].nr_threads) + " - " + list_signals_labels[idx_sig], "block size", list_y_labels[idx_sig], enforced_y_limit=list_y_limit[idx_sig])

            # csv output
            tmp_target_file_name = "output_msize_" + str(m_size) + ".txt"
            tmp_target_file_path = os.path.join(target_folder_data, tmp_target_file_name)
            write_stats_data_mean(tmp_target_file_path, arr_types, tmp_stat_objs_per_type, list_signals, "block_size", unique_block_sizes)
