#!/usr/bin/python3.6

import os, sys
import subprocess
import numpy as np

# flags to control what will be done -> provides the possibility to run on cluster but debug on laptop :)
COMPILE_AND_RUN_APP     = True
RUN_ANALYSIS            = False

# hybrid execution parameters
NUM_THREADS             = 4
NUM_ITERS               = 1
EXEC_SETTINGS           = "OMP_NUM_THREADS=" + str(NUM_THREADS) + " OMP_PLACES=cores OMP_PROC_BIND=spread I_MPI_PIN=1 I_MPI_PIN_DOMAIN=auto mpiexec.hydra -np 2 -genvall "
# EXEC_SETTINGS           = "OMP_NUM_THREADS=" + str(NUM_THREADS) + " OMP_PLACES=cores OMP_PROC_BIND=spread I_MPI_PIN=1 I_MPI_PIN_DOMAIN=auto mpiexec -np 2 -genvall "

# APP_NAMES               = ['exec_mpi_sr_task_comm_thread', 'exec_mpi_sr_task', 'exec_mpi_sr_parallel']
APP_NAMES               = ['exec_mpi_sr_parallel']

# application parameters
# MATRIX_SIZES            = list([i for i in np.linspace(1600,2100,6)]) # for testing
# MATRIX_SIZES            = [2000] # there seems to be a bug/deadlock when using exec_mpi_sr_task or exec_mpi_sr_task_comm_thread !!!
MATRIX_SIZES            = list([i for i in np.linspace(10000,16000,4)])
BLOCK_SIZE_DEVIDE       = [20]
CHECK_SOLUTION          = 1

# define directories
script_dir              = os.path.dirname(os.path.abspath(__file__))
application_dir         = os.path.join(script_dir, '..', '..', 'examples', 'cholesky', 'task_benchmarks', 'cholesky', 'mpi_omp')
cur_working_dir         = os.getcwd()
# make sure that common stuff is loaded. Dont worry about the warning that will be shown.. it works
sys.path.append(os.path.join(script_dir, '..', 'common'))
import CChameleonStats as ch_stats

def runAnalysis():
    os.system("rm -f output_*")

    if COMPILE_AND_RUN_APP:
        # first delete intermediate files
        os.chdir(application_dir)
        # compile application
        os.system("make clean")
        os.system("make all")
        
        for tmp_app in APP_NAMES:
            for cur_mat_size in MATRIX_SIZES:
                cur_mat_size = int(cur_mat_size)
                for cur_block_size_divide in BLOCK_SIZE_DEVIDE:
                    cur_b_size = int(cur_mat_size / cur_block_size_divide)
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

    # if RUN_ANALYSIS: TODO

# ======================= Start of Main Here =========================
if __name__ == "__main__":
    # name_suffix = sys.argv[1]
    # run analyis
    runAnalysis()


