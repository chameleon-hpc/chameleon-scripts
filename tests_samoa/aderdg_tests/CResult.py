import os
import numpy as np


class CResult():
  def __init_(self):
    self.n_ranks = 0
    self.n_threads = 0
    self.n_repetition = 0
    self.stealing = 0

    self.task_execution_times = []
    self.max_execution_times = []
    self.avg_execution_times = []   
    self.imbalance = []

  def parseFile(self, file_path):
    cur_file_name = os.path.basename(file_path)
    cur_file_name = os.path.splitext(cur_file_name)[0]
    tmp_split = cur_file_name.split("_")
    
    self.n_repetition = int( tmp_split[-1].strip()[-1:] )
    self.n_threads = int( tmp_split[-2].strip()[1:] )
 
    if("no_stealing" in cur_file_name):
      self.stealing = 0
      print "found result without stealing"
    else:
      self.stealing = 1     
      print "found result with stealing"

    with open(file_path) as file:
       for line in file:
          if "_num_overall_ranks" in line:
            tmp_split = line.split("\t")
            self.n_ranks = int(tmp_split[-1].strip())
            break
 
       file.seek(0)

       self.task_execution_times =[[] for r in range(self.n_ranks)]
       for line in file:
         if "_time_task_execution_overall_sum" in line:
             rank = int(line.split("#")[1].split(":")[0])   
             tmp_split = line.split("\t")
             self.task_execution_times[rank].append(float(tmp_split[3].strip()))
               
       data = np.array(self.task_execution_times);
       #print (np.mean(data,0))
       #print (np.amax(data,0))
       #print (np.argmax(data,0))

       self.imbalance = np.divide(np.amax(data,0),np.mean(data,0))-1
       #print self.imbalance
