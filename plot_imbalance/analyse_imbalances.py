#!/usr/bin/python3.6

import os,sys
import numpy as np
import matplotlib.pyplot as plt

script_dir              = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(script_dir, '..', 'common'))
import CChameleonStats as ch_stats


def computeLoadImbalance(input_file_path, nranks):
  tmp_arr = []
  with open(input_file_path) as file: 
    for line in file:
      tmp_arr.append(line)

  rank_stats = [ch_stats.ChameleonStatsPerRank(i, False) for i in range(nranks)]
  for stats in rank_stats:
     stats.parseContent(tmp_arr, pre_filtered=False)

  data = np.array([stats.task_exec_overall.time_sum for stats in rank_stats])
  #print (np.mean(data,0))  
  #print (np.amax(data,0))
  #print (np.argmax(data,0))
 
  load_imbalance = np.divide(np.amax(data,0),np.mean(data,0))-1

  return load_imbalance

if __name__ == "__main__":
  input_file = sys.argv[1]
  print (input_file)
  ranks = int(sys.argv[2])

  load_imbalance = computeLoadImbalance(input_file, nranks)

  plt.plot(range(0,np.size(load_imbalance)), load_imbalance)
  plt.show()
