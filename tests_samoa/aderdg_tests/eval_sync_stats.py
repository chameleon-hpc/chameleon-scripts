import os,sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from CResult import *

script_dir ="/home/ps659535/chameleon/chameleon-scripts"
print(os.path.join(script_dir, 'plot_imbalance'))
sys.path.append(os.path.join(script_dir, 'plot_imbalance'))
from analyse_imbalances import *

imbalance_threshold = 0.5

def printOutliers(result):
 for i in range(0,np.size(result.imbalance)):
   if(result.imbalance[i]>imbalance_threshold): 
     print ("i:",i," imbalance ",result.imbalance[i])
     for r in range(0,result.n_ranks):
       print "  r:",r, " time: ", result.task_execution_times[r][i]


def plotImbalance(imbalance_stealing, imbalance_nostealing, output_file_path, text_header):
 xtick = range(0, np.size(imbalance_stealing))

 fig = plt.figure(figsize=(16,9),frameon=False)
 ax = fig.gca()

 ax.set_title(text_header)
 ax.set_xlabel("time step")
 ax.set_ylabel("load imbalance") 
 ax.set_ylim([0,2])
  
 ax.plot(range(0, np.size(imbalance_stealing)), imbalance_stealing, color="g", label="stealing enabled")
 ax.plot(range(0, np.size(imbalance_nostealing)), imbalance_nostealing, color="r", label="stealing disabled")
 
 ax.legend(fancybox=True, shadow=False)

 plt.savefig(output_file_path+"_imbalance.png", bbox_inches="tight")  
# plt.show() 
 plt.close(fig)

def plotExecutionScatter(result, outputFile):
 fig = plt.figure(figsize=(16,9),frameon=False)
 ax = fig.gca()
 
 colors = cm.rainbow(np.linspace(0, 1, len(result.task_execution_times)))
 
 for rank_exec_list,c in zip(result.task_execution_times,colors): 
  ax.scatter(range(0,len(rank_exec_list)),rank_exec_list, color=c)

 ax.set_xlabel('Time Step')
 ax.set_ylabel('Overall Task Execution Time')
 ax.set_ylim([0,2])
 plt.savefig(outputFile, bbox_inches="tight")
 plt.show()
 plt.close(fig)

def parseData(source_dir):
  list_results = []  

  for file in os.listdir(source_dir):
    if file.endswith(".log"):
      print(os.path.join(source_dir, file))
      tmp_result = CResult()
      tmp_result.parseFile(os.path.join(source_dir, file))
      #print (tmp_result.task_execution_times)
      list_results.append(tmp_result)
  return list_results

if __name__ == "__main__":

 source_file = sys.argv[1]
 ranks = 32
 threads = 2

 result = fileToLoadImbalanceResult(source_file, ranks, threads)

 print (result.mean_imbalance)
 #source_dir_stealing = sys.argv[2]
 #plot_dir = sys.argv[3]

 #target_folder_plot  = os.path.join(plot_dir, "result_plots")

 #if not os.path.exists(target_folder_plot):
 #  os.makedirs(target_folder_plot)

 
 

 #list_results = []
  
 #list_results+=(parseData(source_dir_nostealing))
 #list_results+=(parseData(source_dir_stealing))

 #print (list_results)

 #nthreads = [1, 2, 4, 8, 16]

 #for t in nthreads:
 #p_res_nostealing = [x for x in list_results if x.stealing==0] 
 #p_res_stealing = [x for x in list_results if x.stealing==1] 
     
 # plotData(p_res_stealing[0].imbalance, p_res_nostealing[0].imbalance, target_folder_plot+"/t"+str(24), str(24)+" threads" )
 #plotExecutionScatter(p_res_nostealing[0],"nostealing.pdf")
 #plotExecutionScatter(p_res_stealing[0],"stealing.pdf")

 #p_res_outliers = [x for x in list_results if x.n_threads==8 and x.stealing==1 and x.n_ranks==32]
 #printOutliers(p_res_outliers[0])

# imbalances_no_stealing= computeLoadImbalance(os.path.join(source_dir, "results_no_stealing_t1_r1.log"), 32)
# imbalances_stealing= computeLoadImbalance(os.path.join(source_dir, "results_stealing_t1_r1.log"), 32)
# print (imbalances_no_stealing)
# print (imbalances_stealing)

# plt.plot(range(0,np.size(imbalances_no_stealing)), imbalances_no_stealing)
# plt.plot(range(0,np.size(imbalances_stealing)), imbalances_stealing)
# plt.show()

