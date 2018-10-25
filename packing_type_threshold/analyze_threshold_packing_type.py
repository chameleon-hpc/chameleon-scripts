#!/usr/bin/python3.6

import os, sys
import subprocess
import numpy as np

# flags to control what will be done -> provides the possibility to run on cluster but debug on laptop :)
COMPILE_AND_RUN_APP     = True
RUN_ANALYSIS            = False

NUM_THREADS             = 4
NUM_ITERS               = 2

def runAnalysis(name_suffix):
    # define directories
    script_dir          = os.path.dirname(os.path.abspath(__file__))
    application_dir     = os.path.join(script_dir, '..', '..', 'examples', 'matrix_example')
    cur_working_dir     = os.getcwd()

    # make sure that common stuff is loaded. Dont worry about the warning that will be shown.. it works
    sys.path.append(os.path.join(script_dir, '..', 'common'))
    import CChameleonStats as ch_stats

    if COMPILE_AND_RUN_APP:
        # first delete intermediate files
        os.chdir(application_dir)
        os.system("rm -f output_" + name_suffix + "_size_*")
        # compile application
        os.system("make")
        
        for cur_size in arr_sizes:
            for n_iter in range(NUM_ITERS):
                tmp_file_name = "output_" + name_suffix + "_size_" + str(cur_size) + "_iter_" + str(n_iter)
                tmp_file_name_orig = os.path.join(cur_working_dir, tmp_file_name + "_orig")
                tmp_file_path = os.path.join(cur_working_dir, tmp_file_name)
                print("Executing " + tmp_file_name, flush=True)
                # execute application & filter for stats
                #os.system("OMP_NUM_THREADS=" + str(NUM_THREADS) + " OMP_PLACES=cores OMP_PROC_BIND=spread I_MPI_PIN=1 I_MPI_PIN_DOMAIN=auto mpiexec.hydra -np 2 -genvall ./main " + str(cur_size) + " 100 0 &> " + tmp_file_name_orig)
                os.system("OMP_NUM_THREADS=" + str(NUM_THREADS) + " OMP_PLACES=cores OMP_PROC_BIND=spread I_MPI_PIN=1 I_MPI_PIN_DOMAIN=auto mpiexec -np 2 -genvall ./main " + str(cur_size) + " 100 0 &> " + tmp_file_name_orig)
                os.system("grep \"Stats R#\" " + tmp_file_name_orig + " > " + tmp_file_path)
                os.system("rm -f tmp_file_output")
        os.chdir(cur_working_dir)

    if RUN_ANALYSIS:
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

        for cur_size in arr_sizes:
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
            for cur_s in arr_sizes:
                file.write(str(cur_s) + ";")
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
            file.write("\n")


# ======================= Start of Main Here =========================
if __name__ == "__main__":

    # define sizes that should be tested
    # arr_sizes               = list([i for i in np.linspace(200,1200,6)])
    # arr_sizes               = list([i for i in np.arange(100,1201,100)])
    # arr_sizes               = [200, 300]
    arr_sizes               = [200]

    name_suffix = sys.argv[1]
    # run analyis
    runAnalysis(name_suffix)


