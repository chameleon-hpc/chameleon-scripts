import os,sys
import numpy as np
import matplotlib.pyplot as plt
import statistics as st

from CResult import *

script_dir ="/home/ps659535/chameleon/chameleon-scripts"

#imbalance_threshold = 0.5

#def printOutliers(result):
# for i in range(0,np.size(result.imbalance)):
#   if(result.imbalance[i]>imbalance_threshold): 
#     print ("i:",i," imbalance ",result.imbalance[i])
#     for r in range(0,result.n_ranks):
#       print "  r:",r, " time: ", result.task_execution_times[r][i]


def plotTimes( xvals, times_r0, times_r1, times_r2, output_file_path, text_header):

 fig = plt.figure(figsize=(16,9),frameon=False)
 ax = fig.gca()

 ax.set_title(text_header)
 ax.set_xlabel("Ranks")
 ax.set_ylabel("Phase time [s]") 
 #ax.set_yscale('log')
 ax.set_xscale('log') 
 
 ax.plot(xvals, times_r0, color="g", label="no replication")
 ax.plot(xvals, times_r1, color="b", label="replication without remote task cancellation")
 ax.plot(xvals, times_r2, color="r", label="replication with remote task cancellation")
 
 ax.legend(fancybox=True, shadow=False)

 plt.savefig(output_file_path+"_time.png", bbox_inches="tight")  
 plt.show() 
 plt.close(fig)

if __name__ == "__main__":

 base_dir = sys.argv[1]
 target_folder_plot  = os.path.join(base_dir, "result_plots")

 if not os.path.exists(target_folder_plot):
   os.makedirs(target_folder_plot)

 list_results = []
 ranks = [1,2,4,8,16,32]  

 #collect all results
 for rep_mode in range(3):
   for nrank in ranks: 
     path = os.path.join(base_dir, str(nrank)+"procs_rep_"+str(rep_mode))
     print ("collecting data in path:",path)
     for file in os.listdir(path):
       if file.endswith(".log"):
         print(os.path.join(path, file))
         tmp_result = CResult()
         tmp_result.parseFile(os.path.join(path, file))
         tmp_result.rep_mode = rep_mode
         list_results.append(tmp_result)

 threads = [1,2,4,8,16]
 ranks = [1,2,4,8,16,32]
 stealing = [0,1]

 for s in stealing:
   for t in threads:
     p_list = []
     for rep_mode in range(3):
       p_list.append([x for x in list_results if x.rep_mode==rep_mode and x.n_threads==t and x.stealing==s])
       p_list[rep_mode] = sorted(p_list[rep_mode], key= lambda elem : elem.n_ranks)

     times_rep0 =[]
     times_rep1 =[]
     times_rep2 =[]
     for r in ranks:
       times_rep0.append( st.mean([x.samoa_phase_time for x in p_list[0] if x.n_ranks==r]) )
       times_rep1.append( st.mean([x.samoa_phase_time for x in p_list[1] if x.n_ranks==r]) )
       times_rep2.append( st.mean([x.samoa_phase_time for x in p_list[2] if x.n_ranks==r]) )

     plotTimes(ranks, times_rep0, times_rep1, times_rep2, target_folder_plot+"/t"+str(t)+"_s"+str(s), "threads="+str(t)+" stealing="+str(s)) 
