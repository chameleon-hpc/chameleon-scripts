import sys
import getopt
import matplotlib.pyplot as plt
import matplotlib
import os

from filter_csv import *

markers_times = 'x'
markers_efficiency = 'o'
markers_imbalance = 'o'

colors = ['#1f77b4','#ff7f0e','#2ca02c']

def plot_speedup_curve(ax,x,base_time, times, label, marker):
 speedups = [ base_time/t for t in times]
 ax.plot(x,speedups,label=label,marker=marker,markerfacecolor="none")

def plot_times_curve(ax,x,times,label, marker,color):
 print(x)
 print(times)
 ax.plot(x,times,label=label,marker=marker, color=color)

def plot_times_curve_error(ax,x,times,label, marker,color,yerr):
 print (yerr)
 ax.errorbar(x,times,label=label,marker=marker, color=color,yerr=yerr)

def plot_efficiency_curve(ax,x, base_time, times, label, marker):
 speedups = [ base_time/t for t in times]
 efficiencies = [ r[1]/r[0] for r in zip(x,speedups)]
 print (efficiencies)
 ax.plot(x,efficiencies,label=label,marker=marker,markerfacecolor="none")

def plot_imbalance_curve(ax, x, imbalance, label, marker,color):
 ax.plot(x,imbalance,label=label,marker=marker,linestyle="dotted",markerfacecolor="none",color=color)
  

def main():
 plot_times = False
 plot_efficiency = False
 plot_speedup = False 
 plot_imbalance = False

 output_filename = "plot.pdf"

 x_filter = "ranks"
 x_label = "Nodes"

 labels = []

 color_offset = 0

 try: 
    opts, arg = getopt.getopt(sys.argv[1:], "i:c:f:o:tsebl:x:","xlabel=")
 except getopt.GetoptError as err:
    print(str(err))
    sys.exit(2)
 file=""
 for o, a in opts:
   if o=="-i":
     file=a
 filter=[]
 for o, a in opts:
   if o=="-f":
     filter=a.split(";")
   if o=="-e":
     plot_efficiency = True
   if o=="-t":
     plot_times = True
   if o=="-l":
     labels=a.split(";")
   if o=="-s":
     plot_speedup = True
   if o=="-o":
     output_filename = a
   if o=="-b":
     plot_imbalance = True
   if o=="-x":
     x_filter = a
   if o=="--xlabel":
     x_label = a


 if labels==[]:
   labels = filter
 #x=[1,2,4,8,16,32,56,128,256,512]

 #times with CCP
 fig = plt.figure()
 ax = fig.add_subplot(111)
 ax.set_xscale('log', basex=2)
 ax.set_yscale('log', basey=2)
 #ax.set
 
 curr_ax = ax

 cnt = 0 
 if plot_times:
   print("plotting times")
   for f in filter:
     print (f)
     dict=getSortedDict(file,f,"",x_filter)
     print (dict)
     times=extractCol(dict, "min_time")
     print (times)
     err=extractCol(dict, "std_dev")
     x=extractCol(dict, x_filter)
     curr_ax.set_xticks(x)
     curr_ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
     curr_ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
     plot_times_curve(curr_ax, x,times, labels[cnt]+" - wall clock time",markers_times, colors[color_offset+cnt])
     #plot_times_curve_error(curr_ax, x,times, labels[cnt]+" - wall clock time", markers_times, colors[color_offset+cnt],err)
     cnt = cnt+1
   curr_ax.legend(frameon=False, loc='lower left',fontsize='small')
   #curr_ax.set_ylim([0.0,1024.0])
   curr_ax.set_xlabel(x_label)
   curr_ax.set_ylabel("Wall Clock Execution Time [s]")

 if plot_speedup:
   if cnt>0:
     cnt = 0
     curr_ax = ax.twinx()

   for f in filter:
     #print (f)
     dict=getSortedDict(file,f,"",x_filter)
     print (dict)
     times=extractCol(dict, "mean_time")
     x=extractCol(dict, x_filter)
     curr_ax.set_xticks(x)
     curr_ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
     plot_speedup_curve(x,times[0], times, labels[cnt],'x')
     cnt = cnt+1
   curr_ax.legend(frameon=False)


 if plot_efficiency:
   if cnt>0:
     cnt = 0
     curr_ax = ax.twinx()
   
   for f in filter:
     #print (f)
     dict=getSortedDict(file,f,"",x_filter)
     print (dict)
     times=extractCol(dict, "mean_time")
     x=extractCol(dict, x_filter)
     curr_ax.set_xticks(x)
     curr_ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
     plot_efficiency_curve(curr_ax,x,times[0], times, labels[cnt]+" - parallel efficiency",markers_efficiency)
     cnt = cnt+1
   curr_ax.set_ylim([0,1.19])
   curr_ax.set_ylabel("Parallel Efficiency")
   curr_ax.legend(frameon=False, loc='upper right', fontsize='small')
 
 if plot_imbalance:
   if cnt>0:
     cnt = 0
     curr_ax = ax.twinx()
   
   for f in filter:
     #print (f)
     dict=getSortedDict(file,f,"",x_filter)
     print (dict)
     imbalances=extractCol(dict, "avg_imbalance")
     x=extractCol(dict, x_filter)
     curr_ax.set_xticks(x)
     curr_ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
     plot_imbalance_curve(curr_ax,x,imbalances, labels[cnt]+" - imbalance",markers_imbalance,colors[color_offset+cnt])
     cnt = cnt+1
   curr_ax.set_ylim([1.0,2.0])
   curr_ax.set_yscale('linear')
   curr_ax.set_xlabel(x_label)
   curr_ax.set_ylabel("Imbalance (max_load/avg_load)")
   curr_ax.legend(frameon=False, loc='upper right', fontsize='small')
 
 plt.savefig(os.path.join(os.path.split(file)[0], output_filename), bbox_inches='tight')

if __name__=="__main__":
  main()
 
