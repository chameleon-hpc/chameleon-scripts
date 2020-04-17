from __future__ import print_function
import sys
import getopt 
import csv


string_keys=['chameleon','tool','stealing','timeCCP']
int_keys=['dmin','dmax','lbfreq','ranks','threads','min_abs_threshold','sections']
float_keys=['time']

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
    csv_reader = csv.DictReader(csv_file, delimiter=" ")
    for row in csv_reader:
      for key in row:
        row[key]=convert_val(key,row[key])

      fulfillConds = 1
      if len(filter)>0:
        for f in filter:          
          filteredCol=f.split("=")[0]
          value=f.split("=")[1]
          value=convert_val(filteredCol,value)
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

def prettyPrintDictList(dict_list):
  for key in dict_list[0]:
    print (key+"\t", end ='')
  print("")
  for dict in dict_list:
    for key,val in dict.items():
      print(str(val)+"\t", end='')
    print ("\n")


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
