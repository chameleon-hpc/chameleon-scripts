import sys
import getopt 
import csv

string_keys=['chameleon','tool','lbtime']
int_keys=['dmin','dmax','lbfreq','ranks','threads','order','min_abs_threshold','sections']
float_keys=['replication_factor','noise','min_time','max_time','mean_time','avg_imbalance','avg_cell_throughput','std_dev']

def convert_val(key,val):
 if key in string_keys:
   return val
 elif key in int_keys:
   return int(val)
 elif key in float_keys:
   return float(val)

def extractCol(dict,col):
 vals=[]
 for d in dict:
   vals.append(d[col])
 return vals

def getSortedDict(file,filter,cols,sort):
 if filter!="":
  filter=filter.split(",")
 if cols!="":
  cols=cols.split(",")
 if sort!="":
  sort=sort.split(',')
 
 dict=readIntoDict(file,cols,filter)
 return sortDict(dict,sort)

def sortDict(dict,sort):
 if(len(sort)>0):
   for s in sort:
     dict.sort(key=lambda x: x[s])
 return dict

def readIntoDict(file,cols,filter=""):
 result=[]

 with open(file,mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter="\t")
    for row in csv_reader:
      #print (row)
      for key in row:
        row[key]=convert_val(key,row[key])

      fulfillConds = 1
      if len(filter)>0:
        for f in filter:          
          filteredCol=f.split("=")[0]
          #print (f)
          value=f.split("=")[1]
          value=convert_val(filteredCol,value)
          #print (filteredCol, value)
          #print (row)
          if(row[filteredCol]!=value):
            fulfillConds=0
            break
      if fulfillConds:
        result.append(row)
 return result

def writeDictToFile(file,dict,cols):
  with open(file, mode='w') as output_file:
    writer = csv.DictWriter(output_file, delimiter=" ", fieldnames=cols,
                            extrasaction='ignore')  
    
    writer.writeheader()
    for d in dict:
      writer.writerow(d)         

def main():
 try: 
    opts, arg = getopt.getopt(sys.argv[1:], "i:c:s:f:o:")
 except getopt.GetoptError as err:
    print(str(err))
    sys.exit(2)
 file=""
 cols=""
 sort=""
 conds=""
 output=""
 for o, a in opts:
   if o=="-i":
     file=a
   elif o=="-c":
     cols=a
   elif o=="-s":
     sort=a
   elif o=="-f":
     conds=a
   elif o=="-o":
     output=a

 sort=sort.split(",")
 cols=cols.split(",")
 if conds!="":
   conds=conds.split(",")
 print(file,cols,sort,conds)

 dict = readIntoDict(file,cols,conds)
 dict = sortDict(dict,sort)
 print(dict) 
 writeDictToFile(output,dict,cols)

if __name__=="__main__":
  main()
