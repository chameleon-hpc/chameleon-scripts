import sys
import getopt
import matplotlib.pyplot as plt
import matplotlib
from filter_csv import *

def plot_speedup_curve(x,base_time, times, label, marker, color='b'):
 speedups = [ base_time/t for t in times]
 plt.plot(x,speedups,label=label,marker=marker,markerfacecolor="none",color=color)

def plot_times(x,times,label, marker):
 plt.plot(x,times,label=label,marker=marker)

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

 x=[1,2,4,8,16,32]

 #times with CCP
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.set_xscale('log', basex=2)
# ax.set_yscale('log', basey=2)
# #ax.set

 dict=getSortedDict(file,"lbfreq=1,chameleon=yes,min_abs_threshold=0","","ranks")
 times_1_yes_0=extractCol(dict, "time")
 #plot_times(x,times_1_yes_0, "lbfreq=1,chameleon=yes,min_abs_threshold=0",'x')

 dict=getSortedDict(file,"lbfreq=1,chameleon=yes,min_abs_threshold=2","","ranks")
 times_1_yes_2=extractCol(dict, "time")
 #plot_times(x,times_1_yes_2, "lbfreq=1,chameleon=yes,min_abs_threshold=2",'x')

 dict=getSortedDict(file,"lbfreq=1,chameleon=yes,min_abs_threshold=23","","ranks")
 times_1_yes_23=extractCol(dict, "time")
 #plot_times(x,times_1_yes_23, "lbfreq=1,chameleon=yes,min_abs_threshold=23",'x')

 dict=getSortedDict(file,"lbfreq=1,chameleon=no,threads=24","","ranks")
 print(dict)
 times_1_no_24=extractCol(dict, "time")
 #plot_times(x,times_1_no_24, "lbfreq=1,chameleon=no,threads=24",'x')

 dict=getSortedDict(file,"lbfreq=1,chameleon=no,threads=23","","ranks")
 print(dict)
 times_1_no_23=extractCol(dict, "time")
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

 dict=getSortedDict(file,"lbfreq=1000000,chameleon=yes,tool=no,min_abs_threshold=0","","ranks")
 times_1000000_yes_0=extractCol(dict, "time")
 #plot_times(x,times_1000000_yes_0, "lbfreq=1000000,chameleon=yes,min_abs_threshold=0",'x')

 dict=getSortedDict(file,"lbfreq=1000000,chameleon=yes,tool=no,min_abs_threshold=2","","ranks")
 times_1000000_yes_2=extractCol(dict, "time")
 #plot_times(x,times_1000000_yes_2, "lbfreq=1000000,chameleon=yes,min_abs_threshold=2",'x')

 dict=getSortedDict(file,"lbfreq=1000000,chameleon=yes,tool=no,min_abs_threshold=23","","ranks")
 times_1000000_yes_23=extractCol(dict, "time")

 dict=getSortedDict(file,"lbfreq=1000000,chameleon=yes,tool=yes,min_abs_threshold=23","","ranks")
 print(dict)
 times_1000000_yes_23_tool=extractCol(dict, "time")
 #plot_times(x,times_1000000_yes_23, "lbfreq=1000000,chameleon=yes,min_abs_threshold=23",'x')

 dict=getSortedDict(file,"lbfreq=1000000,chameleon=no,threads=24","","ranks")
 print(dict)
 times_1000000_no_24=extractCol(dict, "time")
 #plot_times(x,times_1000000_no_24, "lbfreq=1000000,chameleon=no,threads=24",'x')

 dict=getSortedDict(file,"lbfreq=1000000,chameleon=no,threads=23","","ranks")
 print(dict)
 times_1000000_no_23=extractCol(dict, "time")
 #plot_times(x,times_1000000_no_23,"lbfreq=1000000,chameleon=no,threads=23",'x')

# ax.set_xticks([1,2,4,8,16,32])
# ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
# plt.legend()
# plt.show()
 
 #speedups with CCP
 fig = plt.figure()
 ax = fig.add_subplot(111)
 ax.set_xscale('log', basex=2)
 ax.set_yscale('log', basey=2)
 ax.set_xticks([1,2,4,8,16,32])
 ax.set_yticks([1,2,4,8,16,32])
 ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
 ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

 #ideal curve
 plt.plot(x,x, label='ideal speedup')
 plot_speedup_curve(x,times_1_no_24[0],times_1_no_24,"baseline, 24 threads",'x')
 plot_speedup_curve(x,times_1_no_24[0],times_1_yes_23,"reactive loadbalancing, sorting, 23 threads",'x')
 #plot_speedup_curve(x,times_1_no_24[0],times_1_yes_2,"balanced, chameleon,min_abs_threshold=2 ",'x')
 #plot_speedup_curve(x,times_1_no_24[0],times_1_yes_2,"balanced, chameleon,min_abs_threshold=0 ",'x')
 plt.legend(frameon=False)
 plt.ylabel('relative speedup to single-node baseline')
 plt.xlabel('#nodes')
 plt.savefig('speedup_ccp.pdf', bbox_inches='tight')
 plt.show()

 #speedups without CCP
 fig = plt.figure()
 ax = fig.add_subplot(111)
 ax.set_xscale('log', basex=2)
 ax.set_yscale('log', basey=2)
 ax.set_xticks([1,2,4,8,16,32])
 ax.set_yticks([1,2,4,8,16,32])
 ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
 ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

 #ideal curve
 plt.plot(x,x,label='ideal speedup',color='k')
 plot_speedup_curve(x,times_1000000_no_24[0],times_1000000_no_24,"baseline, 24 threads",'^','r')
 plot_speedup_curve(x,times_1000000_no_24[0],times_1000000_yes_23,"reactive loadbalancing, sort-based, 23 threads ",'s','b')
 plot_speedup_curve(x,times_1000000_no_24[0],times_1000000_yes_23_tool,"reactive loadbalancing, lowest, 23 threads",'o','g') 
 #plot_speedup_curve(x,times_1000000_no_24[0],times_1000000_yes_2,"imbalanced, chameleon,min_abs_threshold=2 ",'x')
 #plot_speedup_curve(x,times_1000000_no_24[0],times_1000000_yes_2,"imbalanced, chameleon,min_abs_threshold=0 ",'x')
 plt.legend(frameon=False)
 plt.ylabel('relative speedup to single-node baseline')
 plt.xlabel('#nodes')
 plt.savefig('speedup_no_ccp.pdf', bbox_inches='tight')
 plt.show()

if __name__=="__main__":
  main()
