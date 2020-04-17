#!/usr/bin/python3.6

import os,sys
import numpy as np
import matplotlib.pyplot as plt
import csv

script_dir              = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(script_dir, '..', 'common'))
import CChameleonStats as ch_stats


class LoadImbalanceResult:
  def __init__(self, ranks, threads, max_exec_times, mean_exec_times, arg_max_exec_times, imbalance, mean_imbalance ):
    self.ranks = ranks
    self.threads = threads
    self.max_exec_times = max_exec_times
    self.mean_exec_times = mean_exec_times
    self.arg_max_exec_times = arg_max_exec_times
    self.imbalance = imbalance
    self.mean_imbalance = mean_imbalance


def fileToLoadImbalanceResult(input_file_path, nranks, nthreads):
  tmp_arr = []
  with open(input_file_path) as file: 
    for line in file:
      tmp_arr.append(line)

  rank_stats = [ch_stats.ChameleonStatsPerRank(i, False) for i in range(nranks)]
  for stats in rank_stats:
     stats.parseContent(tmp_arr, pre_filtered=False)

  data = np.array([stats.task_exec_overall.time_sum for stats in rank_stats])
  cur_max   = np.amax(data,0)
  cur_mean  = np.mean(data,0)
  cur_arg_max = np.argmax(data,0)
 
  load_imbalance = np.divide(cur_max,cur_mean)
  mean_load_imbalance = np.mean(load_imbalance,0)
 
  return LoadImbalanceResult(nranks, nthreads, cur_max, cur_mean, cur_arg_max, load_imbalance, mean_load_imbalance)
  

def parseTaskExecTimes(input_file_path, nranks):
  
  tmp_arr = []
  with open(input_file_path) as file: 
    for line in file:
      tmp_arr.append(line)

  rank_stats = [ch_stats.CChameleonStatsPerRank(i, False) for i in range(nranks)]
  for stats in rank_stats:
     stats.parseContent(tmp_arr, pre_filtered=False)

  data = np.array([stats.task_exec_overall.time_sum for stats in rank_stats])
  return data

def computeLoadImbalance(input_file_path, nranks):
  data = parseTaskExecTimes(input_file_path, nranks)   

  cur_max   = np.amax(data,0)
  cur_mean  = np.mean(data,0)
  cur_arg_max = np.argmax(data,0)
  print (cur_mean)  
  print (cur_max)
  print (cur_arg_max)
 
  load_imbalance = np.divide(cur_max,cur_mean)

  tmp_target_file_path = os.path.splitext(input_file_path)[0] + "_imbalance.txt"
  print("Writing imbalance csv output to " + tmp_target_file_path)
  
  with open(tmp_target_file_path, mode='w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['Max Values'])
    writer.writerow(cur_max)
    writer.writerow(['Mean Values'])
    writer.writerow(cur_mean)
    writer.writerow(['Argmax Values'])
    writer.writerow(cur_arg_max)
    writer.writerow(['Load Imbalance'])
    writer.writerow(load_imbalance)

  return load_imbalance

if __name__ == "__main__":
  input_file = sys.argv[1]
#   input_file = "C:\\J.Klinkenberg.Local\\repos\\chameleon\\chameleon-scripts\\tests_samoa\\strong_scaling_tests\\imbalances_23threads\\results_stealing_t23_r1_chameleon_strong.log"
#  input_file = "C:\\J.Klinkenberg.Local\\repos\\chameleon\\chameleon-scripts\\tests_samoa\\strong_scaling_tests\\imbalances_12threads\\results_no_stealing_t12_r1_chameleon_strong.log"
#  print (input_file)
  ranks = int(sys.argv[2])
#  ranks = 32

  load_imbalance = computeLoadImbalance(input_file, ranks)

  plt.plot(range(0,np.size(load_imbalance)), load_imbalance)
  plt.show()
