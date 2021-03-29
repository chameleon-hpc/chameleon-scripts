import re
import statistics


class CResultAcc:
  def __init__(self):
    self.chameleon = ""
    self.ranks = -1
    self.threads = -1
    self.lbfreq = -1
    self.sections = -1
    self.dmin = -1
    self.dmax = -1
    self.order = -1
    self.noise = -1
    self.min_time = -1
    self.max_time = -1
    self.mean_time = -1
    self.std_dev = -1
    self.replication_factor = -1
    self.avg_imbalance = -1
    self.avg_cell_throughput = -1
    self.lbtime = -1

  def toString(self):
    return self.chameleon+"\t"+str(self.ranks)+"\t"+str(self.threads)+"\t"+str(self.lbfreq)+"\t"+str(self.lbtime)+"\t"+str(self.sections)+"\t"+str(self.dmin)\
           +"\t"+str(self.dmax)+"\t"+str(self.order)+"\t"+str(self.noise)+"\t"+str(self.replication_factor)+"\t"+str(self.min_time)+"\t"+str(self.max_time)+"\t"+str(self.mean_time)+"\t"+ str(self.std_dev)+"\t"+str(self.avg_imbalance)+"\t"+str(self.avg_cell_throughput)

  def toStringHeader(self):
    return "chameleon\tranks\tthreads\tlbfreq\tlbtime\tsections\tdmin\tdmax\torder\tnoise\treplication_factor\tmin_time\tmax_time\tmean_time\tstd_dev\tavg_imbalance\tavg_cell_throughput"

class CResult:
  def __init__(self):
    self.chameleon = ""
    self.ranks = -1
    self.threads = -1
    self.time = -1
    self.noise = -1
    self.run = -1
    self.lbfreq = -1
    self.sections = -1
    self.dmin = -1
    self.dmax = -1
    self.order = -1
    self.replication_factor = -1
    self.imbalance = -1
    self.cell_throughput = -1
    self.lbtime = -1

  def printRes(self):
    print (self.chameleon,"\t", self.ranks,"\t", self.threads, "\t", self.lbfreq, "\t", self.lbtime, "\t", self.sections, "\t", self.dmin,\
    "\t", self.dmax, "\t", self.order, "\t", self.noise, "\t", self.replication_factor, "\t", self.time, "\t", self.imbalance, "\t", self.cell_throughput)

  def printHeader(self):
    print ("chameleon\tranks\tthreads\tlbfreq\tlbtime\tsections\tdmin\tdmax\torder\tnoise\treplication_factor\trun\ttime\timbalance\tcell_throughput")

  def toStringHeader(self):
    return "chameleon\tranks\tthreads\tlbfreq\tlbtime\tsections\tdmin\tdmax\torder\tnoise\treplication_factor\trun\ttime\timbalance\tcell_throughput"

  def toString(self):
    return self.chameleon+"\t"+str(self.ranks)+"\t"+str(self.threads)+"\t"+str(self.lbfreq)+"\t"+str(self.lbtime)+"\t"+str(self.sections)+"\t"+str(self.dmin)\
        +"\t"+str(self.dmax)+"\t"+str(self.order)+"\t"+str(self.noise)+"\t"+str(self.replication_factor)+"\t"+str(self.run)+"\t"+str(self.time)+"\t"+str(self.imbalance)\
        +"\t"+str(self.cell_throughput)

  def __eq__(self, other):
    return self.chameleon==other.chameleon \
       and self.ranks==other.ranks \
       and self.threads==other.threads \
       and self.lbfreq==other.lbfreq \
       and self.sections==other.sections \
       and self.dmin==other.dmin \
       and self.dmax==other.dmax \
       and self.order==other.order \
       and self.replication_factor==other.replication_factor \
       and self.noise==other.noise \
       and self.lbtime==other.lbtime

  def __hash__(self):
    return hash((self.chameleon,self.ranks,self.threads,self.sections,self.lbfreq,self.lbtime,self.dmin,self.dmax,self.order,self.replication_factor,self.noise))

  def parseResultFromFile(self,filename,filename_err):
    file=open(filename, 'r')

    file_err = open(filename_err,'r')
    #     (r0,t0)  Phase time:                        3089.0989 s
    phase_time_pattern = re.compile(".*Phase time: *([0-9]+\.[0-9]+)") 
    phase_times = []
    #     (r0,t0)  sam(oa): Space filling curves and Adaptive Meshes for Oceanic and Other Applications
    #     (r0,t0)  Scenario: SWE
    #     (r0,t0)  OpenMP: Yes, with tasks, threads: 23, procs: 48
    #     (r0,t0)  MPI: Yes, ranks: 32
    #     (r0,t0)  ASAGI: Yes, without NUMA support, mode: 2: no mpi
    #     (r0,t0)  Debug Level: 1
    #     (r0,t0)  Assertions: Yes
    #     (r0,t0)  Precision: Double
    #     (r0,t0)  Compiler: Intel
    #     (r0,t0)  Sections per thread: 16
    #     (r0,t0)  Adaptivity: min depth: 15, max depth: 25, start depth: 0
    #     (r0,t0)  SWE: Patches: Yes, order: 7, vectorization: Off
    #     (r0,t0)  Load balancing: timed load estimate:  No, split mode: 0, serial:  No, frequency: 100000 , threshold: .010
    #     (r0,t0)  Load balancing: for heterogenous hardware (HH):  No, ratio: 1.0/1.0
    #     (r0,t0)  Load balancing: cell weight: 1.00, boundary weight: .00
    ranks_pattern = re.compile(".*ranks: ([0-9]+)")
    sections_pattern = re.compile(".*Sections per thread: ([0-9]+)")
    threads_pattern = re.compile(".*, threads: ([0-9]+),.*")
    min_max_pattern = re.compile(".*min depth: ([0-9]+), max depth: ([0-9]+)")
    order_pattern = re.compile(".*Patches: Yes, order: ([0-9]+)")
    lbfreq_pattern = re.compile(".* frequency: ([0-9]+)")
    lbtime_pattern = re.compile(".*timed load estimate:.*(Yes|No), split")
    cell_throughput_pattern = re.compile(".*Cell update throughput solver: *([0-9]+\.[0-9]+)")

    threads=-1
    ranks=-1
    dmin=-1
    dmax=-1
    order=-1
    sections=-1
    lbfreq=-1
    throughput=-1

    chameleon="no"
    lbtime="No"

    if "intel_rep" in filename:
      index =filename.find("intel_rep")
      chameleon = filename[index:-4]

    noise=0
    index = filename.find("_n_")
    if(index!=-1):
      index_end = filename[index+3:].find("_")
      noise = int(filename[index+3:index+3+index_end]) 

    run=1
    index = filename.find("_r_")
    if(index!=-1):
      index_end = filename[index+3:].find("_")
      if(index_end==-1):
        index_end = filename[index+3:].find(".")
      run = int(filename[index+3:index+3+index_end])

    replication_factor = 0
    index = filename.find("_repf_")
    if(index!=-1):
      index_end = filename[index+6:].find("_")
      replication_factor = float(filename[index+6:index+6+index_end])

    #print(len(chameleon))

    for line in file:
      m=re.match(phase_time_pattern, line)
      if m:
        phase_times.append(float(m.group(1)))
      m=re.match(ranks_pattern, line)
      if m:
        ranks = int(m.group(1))
        #print m.group(1)
      m=re.match(sections_pattern, line)
      if m:
        sections = int(m.group(1))
      m=re.match(threads_pattern, line)
      if m:
        #print line
        threads = int(m.group(1))
      m=re.match(min_max_pattern, line)
      if m:
        dmin = int(m.group(1))
        dmax = int(m.group(2))
      m=re.match(order_pattern, line)
      if m:
        order = int(m.group(1))
      m=re.match(lbfreq_pattern, line)
      if m:
        lbfreq = int(m.group(1))
      m=re.match(lbtime_pattern, line)
      if m:
        lbtime = m.group(1)
        #print(lbtime)
      m=re.match(cell_throughput_pattern,line)
      if m:
        throughput = float(m.group(1))

    if(len(phase_times)<2):
      time = -1
    else:
      time = phase_times[-1]

    self.chameleon = chameleon
    self.ranks = ranks
    self.threads = threads
    self.sections = sections
    self.lbfreq = lbfreq
    self.lbtime = lbtime
    self.dmin = dmin
    self.dmax = dmax
    self.time = time
    self.noise = noise
    self.order = order
    self.replication_factor = replication_factor
    self.run = run
    self.cell_throughput = throughput

    task_execution_times = [0 for r in range(ranks)] 
    #Stats R#4:   _time_task_execution_overall_sum    sum=    17007.8129334450    count=  750987  mean=   0.0226472801
    found = False

    task_execution_pattern = re.compile("Stats R#([0-9]+).*_time_task_execution_overall_sum.*sum=\t([0-9]*\.[0-9]*).*count.*")
    for line in file_err:
      m=re.match(task_execution_pattern, line)
      if m:
        found = True
        #print (line)
        #print (m.group(1), m.group(2))
        task_execution_times[int(m.group(1))]=float(m.group(2))

    if(found):
      self.imbalance = max(task_execution_times)/statistics.mean(task_execution_times)
    #print (self.imbalance)

