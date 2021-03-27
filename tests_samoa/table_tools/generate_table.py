from CResult import *
import os
import sys
import statistics

def gatherResults(folder):
  results = []

  for f in os.listdir(folder):
    if "out" in f:
      result= CResult()
      result.parseResultFromFile(os.path.join(folder,f), os.path.join(folder, "err_"+f[4:]))
      if(result.ranks==-1):
         print (f)
      if(result.ranks!=-1):
        results.append(result)
  return results


def writeResults(folder, filename, results):
  output_file = os.path.join(folder, filename)
  with open(output_file, "w") as f:
    f.write(results[0].toStringHeader()+"\n")
    for r in results:
      #print (r.toString())
      f.write(r.toString()+"\n")
    f.close()

def accumulateResults(results):
  uniqueResults = list(set(results))
  accumulatedResults = []

  for unique in uniqueResults:
    if unique.ranks==-1:
      continue
   
    accResult = CResultAcc()

    accResult.chameleon = unique.chameleon 
    accResult.ranks = unique.ranks
    accResult.threads = unique.threads
    accResult.lbfreq = unique.lbfreq
    accResult.sections = unique.sections
    accResult.dmin = unique.dmin
    accResult.dmax = unique.dmax
    accResult.noise = unique.noise
    accResult.order = unique.order
    accResult.replication_factor = unique.replication_factor

    times = []

    for r in results:
      if r==unique:
        times.append(r.time)
   
    accResult.min_time = min(times)
    accResult.max_time = max(times)
    accResult.mean_time = statistics.mean(times)
    if len(times)>1:
      accResult.std_dev = statistics.stdev(times)
   
    imbalances = []
    for r in results:
      if r==unique:
         imbalances.append(r.imbalance)

    accResult.avg_imbalance = statistics.mean(imbalances)
    
    throughputs = []
    for r in results:
      if r==unique:
         throughputs.append(r.cell_throughput)

    accResult.avg_cell_throughput = statistics.mean(throughputs)

    accumulatedResults.append(accResult)

  return accumulatedResults

if __name__ == "__main__":
  folder = sys.argv[1]
  results = gatherResults(folder)
  accResults = accumulateResults(results)
  writeResults(folder, "table.csv", results)
  writeResults(folder, "table_acc.csv", accResults)
