import sys
import getopt
import matplotlib.pyplot as plt
import matplotlib
from filter_csv import *

markers = ['o','s','+']
colors = ['b','k','r']
labels = ['reactive load balancing','time based domain decomposition','baseline']

def plot_speedup_curve(title, x, base_time, times_base, times_migration, times_ccp, labels, xlabel, ylabel, markers, colors):
 speedups_migration = [ times_migration[0]/t for t in times_migration]
 speedups_timeCCP = [ times_ccp[0]/t for t in times_ccp ]
 speedups_base = [ times_base[0]/t for t in times_base ]
 plt.plot(x,speedups_migration,label=labels[0],marker=markers[0],markerfacecolor="none",color=colors[0])
 plt.plot(x,speedups_timeCCP,label=labels[1],marker=markers[1],markerfacecolor="none",color=colors[1])
 plt.plot(x,speedups_base,label=labels[2],marker=markers[2],markerfacecolor="none",color=colors[2])
 plt.legend(loc="upper left")
 plt.xlabel(xlabel)
 plt.ylabel(ylabel)
 plt.title(title)
 plt.xscale('log',basex=2)
 #plt.show()

def plot_speedup_to_base(title, x, times_base, times_migration, times_ccp, labels, xlabel, ylabel, markers, colors):
 speedups_migration = [ tb/t for tb,t in zip(times_base,times_migration)]
 speedups_timeCCP = [ tb/t for tb,t in zip(times_base,times_ccp) ]
 plt.plot(x,speedups_migration,label=labels[0],marker=markers[0],markerfacecolor="none",color=colors[0])
 plt.plot(x,speedups_timeCCP,label=labels[1],marker=markers[1],markerfacecolor="none",color=colors[1])
 plt.legend(loc="lower right")
 plt.xlabel(xlabel)
 plt.ylabel(ylabel)
 plt.title(title)
 plt.xscale('log',basex=2)
 #plt.show()

def plot_times(x, base_times, migration_times, ccp_times, labels, xlabel, ylabel, markers, colors):
 plt.plot(x, base_times, label=labels[0], marker=markers[0], color=colors[0])
 plt.plot(x, migration_times, label=labels[1], marker=markers[1], color=colors[1])
 plt.plot(x, ccp_times, label=labels[2], marker=markers[2], color=colors[2])
 plt.legend(loc="upper right")
 plt.xlabel(xlabel)
 plt.ylabel(ylabel)
 #plt.show()
 
def main():
 try: 
    opts, arg = getopt.getopt(sys.argv[1:], "i:c:s:f:o:")
 except getopt.GetoptError as err:
    print(str(err))
    sys.exit(2)
 file=""
 for o, a in opts:
   if o=="-i":
     file=a

 ranks=[1,2,4,8,16,32,64,128]
 threads=[1,2,4,8,11,23]

 for r in ranks:
   dict=getSortedDict(file,"timeCCP=yes,ranks="+str(r),"","ranks,threads")
   times_ccp=extractCol(dict, "time")
   
   dict=getSortedDict(file,"timeCCP=no,stealing=no,ranks="+str(r),"","ranks,threads")
   times_base=extractCol(dict, "time")
   
   dict=getSortedDict(file,"timeCCP=no,stealing=yes,ranks="+str(r),"","ranks,threads")
   times_steal=extractCol(dict, "time")
   #prettyPrintDictList(dict)

   print times_base,times_steal, times_ccp
   plot_speedup_curve("ranks="+str(r),threads, times_base[0], times_base, times_steal, times_ccp, labels, "threads", "strong scaling speedup", markers, colors)
   plt.savefig("plots/strong_scaling_threads_r"+str(r)+".pdf");
   plt.close()
   plot_speedup_to_base("ranks="+str(r),threads, times_base, times_steal, times_ccp, labels, "threads", "speedup to cell-based domain decomposition baseline", markers, colors)
   plt.savefig("plots/speedup_chameleon_threads_r"+str(r)+".pdf");
   plt.close()

 ranks=[1,2,4,8,16,32,64,128]
 for t in threads:
   dict=getSortedDict(file,"timeCCP=yes,threads="+str(t),"","ranks,threads")
   times_ccp=extractCol(dict, "time")
   
   dict=getSortedDict(file,"timeCCP=no,stealing=no,threads="+str(t),"","ranks,threads")
   times_base=extractCol(dict, "time")
   
   dict=getSortedDict(file,"timeCCP=no,stealing=yes,threads="+str(t),"","ranks,threads")
   times_steal=extractCol(dict, "time")
   
   print times_base,times_steal, times_ccp
   plot_speedup_curve("threads="+str(t), ranks, times_base[0], times_base, times_steal, times_ccp, labels, "ranks", "strong scaling speedup", markers, colors)
   plt.savefig("plots/strong_scaling_ranks_t"+str(t)+".pdf");
   plt.close()
   plot_speedup_to_base("threads="+str(t),ranks, times_base, times_steal, times_ccp, labels, "ranks", "speedup to cell-based domain decomposition baseline", markers, colors)
   plt.savefig("plots/speedup_chameleon_ranks_t"+str(t)+".pdf");
   plt.close()

 #plot_times(x,times_1_yes_0, "lbfreq=1,chameleon=yes,min_abs_threshold=0",'x')

# dict=getSortedDict(file,"lbfreq=1,chameleon=yes,min_abs_threshold=2","","ranks")
# times_1_yes_2=extractCol(dict, "time")
 #plot_times(x,times_1_yes_2, "lbfreq=1,chameleon=yes,min_abs_threshold=2",'x')

# dict=getSortedDict(file,"lbfreq=1,chameleon=yes,min_abs_threshold=23","","ranks")
# times_1_yes_23=extractCol(dict, "time")
 #plot_times(x,times_1_yes_23, "lbfreq=1,chameleon=yes,min_abs_threshold=23",'x')

# dict=getSortedDict(file,"lbfreq=1,chameleon=no,threads=24","","ranks")
# print(dict)
# times_1_no_24=extractCol(dict, "time")
 #plot_times(x,times_1_no_24, "lbfreq=1,chameleon=no,threads=24",'x')

# dict=getSortedDict(file,"lbfreq=1,chameleon=no,threads=23","","ranks")
# print(dict)
# times_1_no_23=extractCol(dict, "time")
 #plot_times(x,times_1_no_23,"lbfreq=1,chameleon=no,threads=23",'x')

# ax.set_xticks([1,2,4,8,16,32])
# ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
# plt.legend()
# plt.show()

# times without CCP
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.set_xscale('log', basex=2)
# ax.set_yscale('log', basey=2)
# ax.set
 #plot_times(x,times_1_yes_0, "lbfreq=1,chameleon=yes,min_abs_threshold=0",'x')

# dict=getSortedDict(file,"lbfreq=1,chameleon=yes,min_abs_threshold=2","","ranks")
# times_1_yes_2=extractCol(dict, "time")
 #plot_times(x,times_1_yes_2, "lbfreq=1,chameleon=yes,min_abs_threshold=2",'x')

# dict=getSortedDict(file,"lbfreq=1,chameleon=yes,min_abs_threshold=23","","ranks")
# times_1_yes_23=extractCol(dict, "time")
 #plot_times(x,times_1_yes_23, "lbfreq=1,chameleon=yes,min_abs_threshold=23",'x')

# dict=getSortedDict(file,"lbfreq=1,chameleon=no,threads=24","","ranks")
# print(dict)
# times_1_no_24=extractCol(dict, "time")
 #plot_times(x,times_1_no_24, "lbfreq=1,chameleon=no,threads=24",'x')

# dict=getSortedDict(file,"lbfreq=1,chameleon=no,threads=23","","ranks")
# print(dict)
# times_1_no_23=extractCol(dict, "time")
 #plot_times(x,times_1_no_23,"lbfreq=1,chameleon=no,threads=23",'x')

# ax.set_xticks([1,2,4,8,16,32])
# ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
# plt.legend()
# plt.show()

# times without CCP
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.set_xscale('log', basex=2)
# ax.set_yscale('log', basey=2)
# ax.set

# dict=getSortedDict(file,"lbfreq=1000000,chameleon=yes,tool=no,min_abs_threshold=0","","ranks")
# times_1000000_yes_0=extractCol(dict, "time")
 #plot_times(x,times_1000000_yes_0, "lbfreq=1000000,chameleon=yes,min_abs_threshold=0",'x')

# dict=getSortedDict(file,"lbfreq=1000000,chameleon=yes,tool=no,min_abs_threshold=2","","ranks")
# times_1000000_yes_2=extractCol(dict, "time")
 #plot_times(x,times_1000000_yes_2, "lbfreq=1000000,chameleon=yes,min_abs_threshold=2",'x')

# dict=getSortedDict(file,"lbfreq=1000000,chameleon=yes,tool=no,min_abs_threshold=23","","ranks")
# times_1000000_yes_23=extractCol(dict, "time")

 #dict=getSortedDict(file,"lbfreq=1000000,chameleon=yes,tool=yes,min_abs_threshold=23","","ranks")
 #print(dict)
 #times_1000000_yes_23_tool=extractCol(dict, "time")
 #plot_times(x,times_1000000_yes_23, "lbfreq=1000000,chameleon=yes,min_abs_threshold=23",'x')

 #dict=getSortedDict(file,"lbfreq=1000000,chameleon=no,threads=24","","ranks")
 #print(dict)
 #times_1000000_no_24=extractCol(dict, "time")
 #plot_times(x,times_1000000_no_24, "lbfreq=1000000,chameleon=no,threads=24",'x')

# dict=getSortedDict(file,"lbfreq=1000000,chameleon=no,threads=23","","ranks")
# print(dict)
# times_1000000_no_23=extractCol(dict, "time")
 #plot_times(x,times_1000000_no_23,"lbfreq=1000000,chameleon=no,threads=23",'x')

# ax.set_xticks([1,2,4,8,16,32])
# ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
# plt.legend()
# plt.show()
 
 #speedups with CCP
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.set_xscale('log', basex=2)
# ax.set_yscale('log', basey=2)
# ax.set_xticks([1,2,4,8,16,32])
# ax.set_yticks([1,2,4,8,16,32])
# ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
# ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
#
 #ideal curve
# plt.plot(x,x, label='ideal speedup')
## plot_speedup_curve(x,times_1_no_24[0],times_1_no_24,"baseline, 24 threads",'x')
# plot_speedup_curve(x,times_1_no_24[0],times_1_yes_23,"reactive loadbalancing, sorting, 23 threads",'x')
 #plot_speedup_curve(x,times_1_no_24[0],times_1_yes_2,"balanced, chameleon,min_abs_threshold=2 ",'x')
 #plot_speedup_curve(x,times_1_no_24[0],times_1_yes_2,"balanced, chameleon,min_abs_threshold=0 ",'x')
# plt.legend(frameon=False)
# plt.ylabel('relative speedup to single-node baseline')
# plt.xlabel('#nodes')
# plt.savefig('speedup_ccp.pdf', bbox_inches='tight')
# plt.show()

 #speedups without CCP
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.set_xscale('log', basex=2)
# ax.set_yscale('log', basey=2)
# ax.set_xticks([1,2,4,8,16,32])
# ax.set_yticks([1,2,4,8,16,32])
# ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
# ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

 #ideal curve
# plt.plot(x,x,label='ideal speedup',color='k')
# plot_speedup_curve(x,times_1000000_no_24[0],times_1000000_no_24,"baseline, 24 threads",'^','r')
# plot_speedup_curve(x,times_1000000_no_24[0],times_1000000_yes_23,"reactive loadbalancing, sort-based, 23 threads ",'s','b')
# plot_speedup_curve(x,times_1000000_no_24[0],times_1000000_yes_23_tool,"reactive loadbalancing, lowest, 23 threads",'o','g') 
 #plot_speedup_curve(x,times_1000000_no_24[0],times_1000000_yes_2,"imbalanced, chameleon,min_abs_threshold=2 ",'x')
 #plot_speedup_curve(x,times_1000000_no_24[0],times_1000000_yes_2,"imbalanced, chameleon,min_abs_threshold=0 ",'x')
# plt.legend(frameon=False)
# plt.ylabel('relative speedup to single-node baseline')
# plt.xlabel('#nodes')
# plt.savefig('speedup_no_ccp.pdf', bbox_inches='tight')
# plt.show()

if __name__=="__main__":
  main()
