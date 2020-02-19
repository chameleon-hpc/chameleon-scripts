import os #, sys
import numpy as np
import statistics as st
from datetime import datetime
import csv
import matplotlib.pyplot as plt

from CChameleonStats import *
from CChameleonAggregation import *

def write_stats_data_mean(  tmp_target_file_path, 
                            arr_labels,                 # nx1 array with labels
                            list_meta_objs,             # nx1 array with arrays of objects (Requirement: each object needs to have stats member)
                            arr_signals_to_plot,        # array with signal names
                            field_name_header_value,    # field name that is used for filtering header values
                            arr_header_values,          # mx1 array with header values
                            add_std_dev=True):          # add stddev to output or not

    with open(tmp_target_file_path, mode='w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        
        for sig in arr_signals_to_plot:
            writer.writerow(["===== " + str(sig) + " ====="])
            writer.writerow([str(field_name_header_value)] + arr_header_values)
            for tmp_idx in range(len(arr_labels)):
                sub_list            = list_meta_objs[tmp_idx]
                tmp_arr_mean        = []
                tmp_arr_std_dev     = []
                for hv in arr_header_values:
                    cur_list_stats  = eval("[x.stats for x in sub_list if x." + field_name_header_value + " == " + str(hv) + "]")
                    tmp_vals        = aggregate_chameleon_statistics(cur_list_stats, [sig], aggegration_for_group=EnumAggregationTypeGroup.ALL) # TODO: add aggregation info to interface
                    tmp_vals        = tmp_vals[0] # only need first return value here
                    tmp_arr_mean.append(st.mean(tmp_vals))
                    if add_std_dev:
                        if len(tmp_vals) < 2:
                            tmp_arr_std_dev.append(0)
                        else:
                            tmp_arr_std_dev.append(st.stdev(tmp_vals))
                writer.writerow([arr_labels[tmp_idx] + "_mean"] + tmp_arr_mean)
                if add_std_dev:
                    writer.writerow([arr_labels[tmp_idx] + "_std_dev"] + tmp_arr_std_dev)
            writer.writerow([])