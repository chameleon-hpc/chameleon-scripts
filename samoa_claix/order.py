# import operator
import os
import csv

#!#################################################
test_name = 'NUM_STEPS_Comparison_47Threads_20210824_120750'
rowNames=['Variation','SomeIndex','Group']
#!#################################################

path_to_script = os.path.dirname(os.path.abspath(__file__))
file_path = path_to_script+'/results/'+test_name+'.csv'

out_path = path_to_script+'/results/'+test_name+"_ordered.csv"

for rowName in rowNames:
    with open(file_path, 'r') as f_input:
        csv_input = csv.DictReader(f_input)
        data = sorted(csv_input, key=lambda row: row[rowName])

    with open(out_path, 'w') as f_output:    
        csv_output = csv.DictWriter(f_output, fieldnames=csv_input.fieldnames)
        csv_output.writeheader()
        csv_output.writerows(data)

    os.remove(file_path)
    os.rename(out_path, file_path)