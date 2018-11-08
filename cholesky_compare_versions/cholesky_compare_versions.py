#!/usr/bin/python3.6

import os, sys
import subprocess
import numpy as np
import math

# flags to control what will be done -> provides the possibility to run on cluster but debug on laptop :)
COMPILE_AND_RUN_APP     = True
RUN_ANALYSIS            = True
DELETE_OLD_STUFF        = True

# hybrid execution parameters
NUM_THREADS             = 4
NUM_ITERS               = 10
# local execution on a single node (used for testing)
# EXEC_SETTINGS           = "I_MPI_DEBUG=5 OMP_NUM_THREADS=" + str(NUM_THREADS) + " OMP_PLACES=cores OMP_PROC_BIND=spread I_MPI_PIN=1 I_MPI_PIN_DOMAIN=auto mpiexec.hydra -np 2 -genvall "
# standard execution (single node or multi node depending on how many nodes were requested by batch)
EXEC_SETTINGS           = "I_MPI_DEBUG=5 OMP_NUM_THREADS=" + str(NUM_THREADS) + " OMP_PLACES=cores OMP_PROC_BIND=spread I_MPI_PIN=1 I_MPI_PIN_DOMAIN=auto mpiexec -np 2 -genvall "
# EXEC_SETTINGS           = "I_MPI_DEBUG=5 OMP_NUM_THREADS=" + str(NUM_THREADS) + " OMP_PLACES=cores OMP_PROC_BIND=spread I_MPI_PIN=1 I_MPI_PIN_DOMAIN=auto mpiexec -np 2 --map-by node -report-bindings --bind-to socket --oversubscribe "

# APP_NAMES               = ['exec_mpi_sr_task_comm_thread', 'exec_mpi_sr_task', 'exec_mpi_sr_parallel']
# APP_NAMES               = ['exec_mpi_sr_parallel', 'exec_mpi_sr_task']
APP_NAMES               = ['exec_mpi_sr_task']
# APP_NAMES               = ['exec_mpi_sr_task_comm_thread']

# application parameters
# MATRIX_SIZES            = list([i for i in np.linspace(10000,16000,4)])
# MATRIX_SIZES            = list([i for i in np.arange(10000,20001,20000)])
MATRIX_SIZES            = [10000]
# BLOCK_SIZES             = [5000, 2500, 2000, 1250, 1000, 500, 250]
# BLOCK_SIZES             = [2000, 1000, 500, 250, 125, 100]
BLOCK_SIZES             = [125]
# BLOCK_SIZES             = list([math.ceil(MATRIX_SIZES[0] / i) for i in np.arange(2,61,8)])
# BLOCK_SIZES             = list([i for i in np.arange(100,1001,100)])
CHECK_SOLUTION          = 0

# define directories
script_dir              = os.path.dirname(os.path.abspath(__file__))
application_dir         = os.path.join(script_dir, '..', '..', 'examples', 'cholesky', 'task_benchmarks', 'cholesky', 'mpi_omp')
cur_working_dir         = os.getcwd()

def compileAndRun():
    if DELETE_OLD_STUFF:
        # first delete all previously created output files
        os.system("rm -f output_*")

    # compile application
    os.chdir(application_dir)
    os.system("make clean")
    os.system("make all")
        
    for tmp_app in APP_NAMES:
        for cur_mat_size in MATRIX_SIZES:
            cur_mat_size = int(cur_mat_size)
            for cur_b_size in BLOCK_SIZES:
                cur_b_size = int(cur_b_size)
                for n_iter in range(NUM_ITERS):
                    tmp_file_name           = "output_" + tmp_app + "_mat_" + str(cur_mat_size) + "_block_" + str(cur_b_size) + "_iter_" + str(n_iter)
                    tmp_file_path_orig      = os.path.join(cur_working_dir, tmp_file_name + "_orig")
                    tmp_file_path_stats     = os.path.join(cur_working_dir, tmp_file_name)
                    print("Executing " + tmp_file_name, flush=True)
                    
                    # execute application & filter for stats
                    os.system(str(EXEC_SETTINGS) +  "./" + str(tmp_app) + " " + str(cur_mat_size) + " " + str(cur_b_size) + " " + str(CHECK_SOLUTION) + " &> " + tmp_file_path_orig)
                    os.system("grep \"time:\" " + tmp_file_path_orig + " > " + tmp_file_path_stats)
                    # output on command line once
                    os.system("grep \"time:\" " + tmp_file_path_orig)
    os.chdir(cur_working_dir)
    # os.system("rm *_orig")

def runAnalysis():
    tmp_prefix_results = "result_times_"
    if DELETE_OLD_STUFF:
        # first delete all previously created results
        os.system("rm -f " + tmp_prefix_results + "*")

    for tmp_app in APP_NAMES:
        tmp_path_results = os.path.join(cur_working_dir, tmp_prefix_results + tmp_app + ".txt")
        # init 2D result matrix here
        arr_results_app = np.zeros([len(BLOCK_SIZES), len(MATRIX_SIZES)])
        for i_cur_mat_size in range(len(MATRIX_SIZES)):
            cur_mat_size = int(MATRIX_SIZES[i_cur_mat_size])
            for i_cur_block_size in range(len(BLOCK_SIZES)):
                cur_b_size = BLOCK_SIZES[i_cur_block_size]

                cur_arr_times = []
                for n_iter in range(NUM_ITERS):
                    tmp_file_name           = "output_" + tmp_app + "_mat_" + str(cur_mat_size) + "_block_" + str(cur_b_size) + "_iter_" + str(n_iter)
                    tmp_file_path_stats     = os.path.join(cur_working_dir, tmp_file_name)

                    with open(tmp_file_path_stats, "r") as file:
                        tmp_line = file.readline()
                    
                    # parse line and append time spend
                    cur_spl = tmp_line.split(":")
                    cur_arr_times.append(float(cur_spl[13]))
                
                # calc mean and append add value to 2D array
                arr_results_app[i_cur_block_size, i_cur_mat_size] = np.mean(cur_arr_times)
                
        # save results to corresponding output file
        with open(tmp_path_results, "w") as file:
            # header = matrix sizes
            for cur_ms in MATRIX_SIZES:
                file.write(";" + str(int(cur_ms)))
            file.write("\n")

            # write results
            for i_bs in range(len(BLOCK_SIZES)):
                cur_bs_d = BLOCK_SIZES[i_bs]
                file.write(str(int(cur_bs_d)))
                for i_ms in range(len(MATRIX_SIZES)):
                    cur_ms = MATRIX_SIZES[i_ms]
                    file.write(";" + str(arr_results_app[i_bs, i_ms]))
                file.write("\n")

# ======================= Start of Main Here =========================
if __name__ == "__main__":
    # name_suffix = sys.argv[1]
    
    if COMPILE_AND_RUN_APP:
        compileAndRun()
    
    if RUN_ANALYSIS:
        runAnalysis()