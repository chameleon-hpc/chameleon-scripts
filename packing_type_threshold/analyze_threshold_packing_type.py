#!/usr/bin/python3.6

import os, sys
import subprocess
import numpy as np

# flags to control what will be done -> provides the possibility to run on cluster but debug on laptop :)
COMPILE_AND_RUN_APP     = True
RUN_ANALYSIS            = True

# hybrid execution parameters
NUM_THREADS             = 4
NUM_ITERS               = 2
# local execution on a single node (used for testing)
# EXEC_SETTINGS           = "I_MPI_DEBUG=5 KMP_AFFINITY=verbose OMP_NUM_THREADS=" + str(NUM_THREADS) + " OMP_PLACES=cores OMP_PROC_BIND=spread I_MPI_PIN=1 I_MPI_PIN_DOMAIN=auto mpiexec.hydra -np 2 -genvall "
# standard execution (single node or multi node depending on how many nodes were requested by batch)
EXEC_SETTINGS           = "I_MPI_DEBUG=5 KMP_AFFINITY=verbose OMP_NUM_THREADS=" + str(NUM_THREADS) + " OMP_PLACES=cores OMP_PROC_BIND=spread I_MPI_PIN=1 I_MPI_PIN_DOMAIN=auto mpiexec -np 2 -genvall "

# application parameters
MATRIX_SIZES            = list([2**i for i in range(5, 14)])
NUM_MATRICES            = 20

# define directories
script_dir              = os.path.dirname(os.path.abspath(__file__))
application_dir         = os.path.join(script_dir, '..', '..', 'examples', 'matrix_example')
cur_working_dir         = os.getcwd()

# make sure that common stuff is loaded. Dont worry about the warning that will be shown.. it works
sys.path.append(os.path.join(script_dir, '..', 'common'))
import CChameleonStats as ch_stats

def compileAndRun():
    # first delete intermediate files
    os.chdir(application_dir)
    os.system("rm -f output_" + name_suffix + "_size_*")
    # compile application
    os.system("make clean")
    os.system("make simulate-work")
    
    for cur_size in MATRIX_SIZES:
        for n_iter in range(NUM_ITERS):
            tmp_file_name           = "output_" + name_suffix + "_size_" + str(cur_size) + "_iter_" + str(n_iter)
            tmp_file_name_orig      = os.path.join(cur_working_dir, tmp_file_name + "_orig")
            tmp_file_path           = os.path.join(cur_working_dir, tmp_file_name)
            print("Executing " + tmp_file_name, flush=True)
            # execute application & filter for stats
            os.system(str(EXEC_SETTINGS) + " ./main " + str(cur_size) + " " + str(NUM_MATRICES) + " 0 &> " + tmp_file_name_orig)
            os.system("grep \"Stats R#\" " + tmp_file_name_orig + " > " + tmp_file_path)
    os.chdir(cur_working_dir)

def runAnalysis(name_suffix):

    # arrays for separate measurements
    arr_encode_sum              = []
    arr_encode_avg              = []
    arr_decode_sum              = []
    arr_decode_avg              = []
    arr_offload_send_task_sum   = []
    arr_offload_send_task_avg   = []
    arr_offload_recv_task_sum   = []
    arr_offload_recv_task_avg   = []
    arr_offload_send_res_sum    = []
    arr_offload_send_res_avg    = []
    arr_offload_recv_res_sum    = []
    arr_offload_recv_res_avg    = []

    # combined arrays for sending and receiving of task and corresponding data (includes encode/decode)
    arr_comb_send_task_avg      = []
    arr_comb_recv_task_avg      = []

    for cur_size in MATRIX_SIZES:
        tmp_arr_encode_sum          = []
        tmp_arr_encode_avg          = []
        tmp_arr_decode_sum          = []
        tmp_arr_decode_avg          = []
        tmp_offload_send_task_sum   = []
        tmp_offload_send_task_avg   = []
        tmp_offload_recv_task_sum   = []
        tmp_offload_recv_task_avg   = []
        tmp_offload_send_res_sum    = []
        tmp_offload_send_res_avg    = []
        tmp_offload_recv_res_sum    = []
        tmp_offload_recv_res_avg    = []

        for n_iter in range(NUM_ITERS):
            tmp_file_name = "output_" + name_suffix + "_size_" + str(cur_size) + "_iter_" + str(n_iter)
            # parse statistics
            cur_stats = ch_stats.ChameleonStatsPerRun()
            cur_stats.parseFile(tmp_file_name)

            tmp_arr_encode_sum.append(  cur_stats.stats_per_rank[0].encode.time_sum)
            tmp_arr_encode_avg.append(  cur_stats.stats_per_rank[0].encode.time_avg)
            tmp_arr_decode_sum.append(  cur_stats.stats_per_rank[1].decode.time_sum)
            tmp_arr_decode_avg.append(  cur_stats.stats_per_rank[1].decode.time_avg)

            tmp_offload_send_task_sum.append(   cur_stats.stats_per_rank[0].offload_send_task.time_sum)
            tmp_offload_send_task_avg.append(   cur_stats.stats_per_rank[0].offload_send_task.time_avg)
            tmp_offload_recv_task_sum.append(   cur_stats.stats_per_rank[1].offload_recv_task.time_sum)
            tmp_offload_recv_task_avg.append(   cur_stats.stats_per_rank[1].offload_recv_task.time_avg)

            tmp_offload_send_res_sum.append(    cur_stats.stats_per_rank[1].offload_send_results.time_sum)
            tmp_offload_send_res_avg.append(    cur_stats.stats_per_rank[1].offload_send_results.time_avg)
            tmp_offload_recv_res_sum.append(    cur_stats.stats_per_rank[0].offload_recv_results.time_sum)
            tmp_offload_recv_res_avg.append(    cur_stats.stats_per_rank[0].offload_recv_results.time_avg)
            
            # print("Encode:\tSum\t" + str(cur_stats.stats_per_rank[0].encode.time_sum) + "\tMean\t" + str(cur_stats.stats_per_rank[0].encode.time_avg))
            # print("Decode:\tSum\t" + str(cur_stats.stats_per_rank[1].decode.time_sum) + "\tMean\t" + str(cur_stats.stats_per_rank[1].decode.time_avg))

        # get mean of results
        arr_encode_sum.append(np.mean(tmp_arr_encode_sum))
        arr_encode_avg.append(np.mean(tmp_arr_encode_avg))
        arr_decode_sum.append(np.mean(tmp_arr_decode_sum))
        arr_decode_avg.append(np.mean(tmp_arr_decode_avg))

        arr_offload_send_task_sum.append(np.mean(tmp_offload_send_task_sum))
        arr_offload_send_task_avg.append(np.mean(tmp_offload_send_task_avg))
        arr_offload_recv_task_sum.append(np.mean(tmp_offload_recv_task_sum))
        arr_offload_recv_task_avg.append(np.mean(tmp_offload_recv_task_avg))

        arr_offload_send_res_sum.append(np.mean(tmp_offload_send_res_sum))
        arr_offload_send_res_avg.append(np.mean(tmp_offload_send_res_avg))
        arr_offload_recv_res_sum.append(np.mean(tmp_offload_recv_res_sum))
        arr_offload_recv_res_avg.append(np.mean(tmp_offload_recv_res_avg))

        arr_comb_send_task_avg.append(np.mean(tmp_arr_encode_avg) + np.mean(tmp_offload_send_task_avg))
        arr_comb_recv_task_avg.append(np.mean(tmp_arr_decode_avg) + np.mean(tmp_offload_recv_task_avg))

        # print("Size\t" + str(cur_size) + "\tEncode:\tSum(avg)\t" + format(arr_encode_sum[-1], '.10f') + "\tAvg(avg)\t" + format(arr_encode_avg[-1], '.10f'))
        # print("Size\t" + str(cur_size) + "\tDecode:\tSum(avg)\t" + format(arr_decode_sum[-1], '.10f') + "\tAvg(avg)\t" + format(arr_decode_avg[-1], '.10f'))
        # print("Size\t" + str(cur_size) + "\tOffload_Send_Task:\tSum(avg)\t" + format(arr_offload_send_task_sum[-1], '.10f') + "\tAvg(avg)\t" + format(arr_offload_send_task_avg[-1], '.10f'))
        # print("Size\t" + str(cur_size) + "\tOffload_Recv_Task:\tSum(avg)\t" + format(arr_offload_recv_task_sum[-1], '.10f') + "\tAvg(avg)\t" + format(arr_offload_recv_task_avg[-1], '.10f'))
        # print("Size\t" + str(cur_size) + "\tOffload_Send_Results:\tSum(avg)\t" + format(arr_offload_send_res_sum[-1], '.10f') + "\tAvg(avg)\t" + format(arr_offload_send_res_avg[-1], '.10f'))
        # print("Size\t" + str(cur_size) + "\tOffload_Recv_Results:\tSum(avg)\t" + format(arr_offload_recv_res_sum[-1], '.10f') + "\tAvg(avg)\t" + format(arr_offload_recv_res_avg[-1], '.10f'))
    
    # now write that to a result file
    tmp_res_file_name = "result_analysis_packing_type_" + name_suffix + ".txt"
    with open(tmp_res_file_name, "w") as file:
        file.write("Sizes;")
        for cur_s in MATRIX_SIZES:
            tmp_size_mb = cur_s * cur_s * 8.0 / 1024.0 / 1024.0
            file.write(str(cur_s) + "(" + format(tmp_size_mb, ".2f") + " MiB/matrix);")
        file.write("\n")

        file.write("arr_encode_sum;")
        for tmp in arr_encode_sum:
            file.write(format(tmp, '.10f') + ";")
        file.write("\n")

        file.write("arr_encode_avg;")
        for tmp in arr_encode_avg:
            file.write(format(tmp, '.10f') + ";")
        file.write("\n")

        file.write("arr_decode_sum;")
        for tmp in arr_decode_sum:
            file.write(format(tmp, '.10f') + ";")
        file.write("\n")

        file.write("arr_decode_avg;")
        for tmp in arr_decode_avg:
            file.write(format(tmp, '.10f') + ";")
        file.write("\n")

        file.write("arr_offload_send_task_sum;")
        for tmp in arr_offload_send_task_sum:
            file.write(format(tmp, '.10f') + ";")
        file.write("\n")

        file.write("arr_offload_send_task_avg;")
        for tmp in arr_offload_send_task_avg:
            file.write(format(tmp, '.10f') + ";")
        file.write("\n")

        file.write("arr_offload_recv_task_sum;")
        for tmp in arr_offload_recv_task_sum:
            file.write(format(tmp, '.10f') + ";")
        file.write("\n")

        file.write("arr_offload_recv_task_avg;")
        for tmp in arr_offload_recv_task_avg:
            file.write(format(tmp, '.10f') + ";")
        file.write("\n")

        file.write("arr_offload_send_res_sum;")
        for tmp in arr_offload_send_res_sum:
            file.write(format(tmp, '.10f') + ";")
        file.write("\n")

        file.write("arr_offload_send_res_avg;")
        for tmp in arr_offload_send_res_avg:
            file.write(format(tmp, '.10f') + ";")
        file.write("\n")

        file.write("arr_offload_recv_res_sum;")
        for tmp in arr_offload_recv_res_sum:
            file.write(format(tmp, '.10f') + ";")
        file.write("\n")

        file.write("arr_offload_recv_res_avg;")
        for tmp in arr_offload_recv_res_avg:
            file.write(format(tmp, '.10f') + ";")
        file.write("\n\n")

        file.write("arr_comb_send_task_avg;")
        for tmp in arr_comb_send_task_avg:
            file.write(format(tmp, '.10f') + ";")
        file.write("\n")

        file.write("arr_comb_recv_task_avg;")
        for tmp in arr_comb_recv_task_avg:
            file.write(format(tmp, '.10f') + ";")
        file.write("\n")

# ======================= Start of Main Here =========================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Unsufficient number of arguments\n\n" + 
            "Usage: python3.6 ./analyze_threshold_packing_type.py name [max_exponent]\n" + 
            "  - name           Name for the execution (used as suffix)\n" + 
            "  - max_exponent   (optional) Maximal exponent for array sizes that will be tested (2^x). Default is 13\n")
        exit(2)

    name_suffix = sys.argv[1]

    # check if max val is specified
    if(len(sys.argv) == 3):
        tmp_max_val     = int(sys.argv[2])
        MATRIX_SIZES    = list([2**i for i in range(5, tmp_max_val+1)])

    if COMPILE_AND_RUN_APP:
        compileAndRun()
    
    if RUN_ANALYSIS:
        runAnalysis(name_suffix)


