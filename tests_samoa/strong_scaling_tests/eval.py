import os,sys
import numpy as np
import matplotlib.pyplot as plt
import statistics as st

from CResult import *

script_dir ="/home/ps659535/chameleon/chameleon-scripts"


def plotSpeedup( xranks, baseline_times, stealing_r0, output_file_path, text_header):
 fig = plt.figure(figsize=(16,9),frameon=False)
 ax = fig.gca()
 ax.set_title(text_header)
 ax.set_xlabel("Ranks")
 ax.set_ylabel("Speedup to Chameleon Baseline without Stealing and Replication") 
 ax.set_xticks([1,2,4,8,16,32])

 ax.plot(xranks, np.divide(baseline_times, stealing_r0), label="stealing without replication", marker='x')
# ax.plot(xranks, np.divide(baseline_times, nostealing_r1), label="no stealing with replication",marker='o')
# ax.plot(xranks, np.divide(baseline_times, stealing_r1), label="stealing with replication", marker='x')
# ax.plot(xranks, np.divide(baseline_times, nostealing_r2), label="no stealing with replication + cancellation", marker='o')
# ax.plot(xranks, np.divide(baseline_times, stealing_r2), label="stealing with replication + cancellation", marker='x')

 ax.set_ylim([0,1.5])

 ax.legend(fancybox=True, shadow=False)
 plt.savefig(output_file_path+"_speedup.png", bbox_inches="tight")  
 plt.show()
 plt.close(fig)
 

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
 ranks = [2,4,8,16,32]  

 #collect all results
 for rep_mode in range(1):
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

 threads = [23]
 stealing = [0,1]

 for t in threads:
     p_list = []
     for rep_mode in range(1):
       p_list.append([x for x in list_results if x.rep_mode==rep_mode and x.n_threads==t and x.stealing==0])
       p_list[rep_mode] = sorted(p_list[rep_mode], key= lambda elem : elem.n_ranks)

     times_rep0_no_stealing =[]
     for r in ranks:
       times_rep0_no_stealing.append( st.mean([x.samoa_phase_time for x in p_list[0] if x.n_ranks==r]) )

     p_list = []
     for rep_mode in range(3):
       p_list.append([x for x in list_results if x.rep_mode==rep_mode and x.n_threads==t and x.stealing==1])
       p_list[rep_mode] = sorted(p_list[rep_mode], key= lambda elem : elem.n_ranks)

     times_rep0_stealing =[]
     for r in ranks:
       times_rep0_stealing.append( st.mean([x.samoa_phase_time for x in p_list[0] if x.n_ranks==r]) )
     plotSpeedup(ranks, times_rep0_no_stealing, times_rep0_stealing, target_folder_plot+"/t"+str(t), "threads="+str(t)) 
