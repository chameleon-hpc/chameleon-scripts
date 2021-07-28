#!/usr/bin/python

import os
import re
import numpy as np
import argparse
import itertools

path_to_script = os.path.dirname(os.path.abspath(__file__))
out_path = path_to_script + "/chosenNodes.sh"
out_file = open(out_path, 'w')

topo_path = path_to_script + "/mapping_switches_nodes.log"
topo_file = open(topo_path, 'r')
topo_lines = topo_file.readlines()

# write nodes to ignore here (e.g. when SLURM repeatedly says node x unavailable)
blacklist = ["ncm0113"]

def abort():
    out_file.write("export CHOOSE_NODES_FAILED=1\n")
    topo_file.close()
    out_file.close()
    os._exit(1)

#########################################################
#              Get and parse idle nodes                 #
#########################################################
# fake_input = "c18m         up 30-00:00:0    243   idle ncm[0003,0005,0008,0030,0038,0074-0075,0079,0110,0114,0116-0119,0121-0123,0126,0128-0130,0133-0134,0138,0142-0143,0145,0202-0203,0218,0238-0248,0250-0251,0254-0256,0259,0332-0333,0344-0349,0473-0477,0479-0494,0497-0504,0571,0573-0575,0585-0587,0591-0598,0601,0603-0614,0616,0646,0677,0686,0690,0693-0694,0696-0700,0702-0706,0708,0714,0716,0815-0819,0822-0832,0863-0864,0877-0879,0881-0890,0892-0903,0930-0936,0938],nrm[027-035,037,041-052,069-071,112-113,115-130,132-144,175-176,180,195] \n c18m_low     up 30-00:00:0    243   idle ncm[0003,0005,0008,0030,0038,0074-0075,0079,0110,0114,0116-0119,0121-0123,0126,0128-0130,0133-0134,0138,0142-0143,0145,0202-0203,0218,0238-0248,0250-0251,0254-0256,0259,0332-0333,0344-0349,0473-0477,0479-0494,0497-0504,0571,0573-0575,0585-0587,0591-0598,0601,0603-0614,0616,0646,0677,0686,0690,0693-0694,0696-0700,0702-0706,0708,0714,0716,0815-0819,0822-0832,0863-0864,0877-0879,0881-0890,0892-0903,0930-0936,0938],nrm[027-035,037,041-052,069-071,112-113,115-130,132-144,175-176,180,195]"
# free_nodes = fake_input

free_nodes = os.popen('sinfo | grep c18m | grep idle').read()
if not free_nodes:
    print("All nodes are occupied!")
    abort()
# only take first row (second row is c18m_low)
free_nodes = free_nodes.splitlines()[0]
i_start = free_nodes.find("idle ")+5
free_nodes = free_nodes[i_start:]
free_nodes = free_nodes.strip(" ")
free_nodes = re.split("[\[\]]", free_nodes)
free_nodes = list(filter(None, free_nodes)) # remove empty items
free_nodes = [iterator.strip(' ,') for iterator in free_nodes]
# item i with i=0+2x is the name of the node
# item i+1 are the numbers of the nodes
# convert free_nodes into a list containing all complete names as single items
free_node_list = []
i = 0
while i < len(free_nodes):
    # print(free_nodes[i])
    # only one node
    if free_nodes[i][-1].isdigit() and not free_nodes[i][0].isdigit():
        free_node_list.append(free_nodes[i])
        i = i+1
        continue
    # split the numbers and add the name to all of them
    node_ids = free_nodes[i+1]
    node_ids = node_ids.split(",")
    cur_name = free_nodes[i]
    for cur_range in node_ids:
        # only one id
        if "-" not in cur_range:
            free_node_list.append(cur_name + cur_range)
        # range of ids
        else:
            id_len = len(cur_range.split("-")[0])
            cur_id = int(cur_range.split("-")[0])
            end_id = int(cur_range.split("-")[1])
            while cur_id <= end_id:
                free_node_list.append(cur_name + str(cur_id).zfill(id_len))
                cur_id = cur_id + 1
    i = i+2

print("Currently idling nodes: "+str(len(free_node_list))+"\n")
# print("List of currently idling nodes: "+str(free_node_list)+"\n")

#########################################################
#                   Choose nodes                        #
#########################################################
def checkSameRack(node1, node2): # return 1 if in the same rack, 0 if not, -1 if not in topo file or blacklisted
    # topo_lines = topo_file.readlines()
    if (node1 in blacklist or node2 in blacklist):
        return -1
    linenumber = 0
    linenumber_n1 = -1
    linenumber_n2 = -1
    switch1 = "-1"
    switch2 = "-1"
    line = ""
    while linenumber < len(topo_lines):
        line = topo_lines[linenumber].strip()
        # search for node1
        if node1 in line:
            linenumber_n1 = linenumber
        # search for node2
        if node2 in line:
            linenumber_n2 = linenumber
        if linenumber_n1 > -1 and linenumber_n2 > -1:
            break
        else:
            linenumber +=1
    
    if (linenumber_n1 == -1) or (linenumber_n2 == -1):
        # print("Node "+node1+" or node "+node2+" couldn't be found in topology log-file.")
        # abort()
        return -1
    
    # Search the switch of node1
    while linenumber_n1 > -1:
        if "Switch" in topo_lines[linenumber_n1]:
            start = topo_lines[linenumber_n1].find(":")
            switch1 = topo_lines[linenumber_n1][start:].strip(": =\n\r")
            break
        else:
            linenumber_n1 -= 1
            
    # Search the switch of node1
    while linenumber_n2 > -1:
        if "Switch" in topo_lines[linenumber_n2]:
            start = topo_lines[linenumber_n2].find(":")
            switch2 = topo_lines[linenumber_n2][start:].strip(": =\n\r")
            break
        else:
            linenumber_n2 -= 1
    
    if switch1 == "-1" or switch2 == "-1":
        print("Switch couldn't be found in topology log-file.")
        # abort()
        return -1
    # compare the switches
    if switch1 == switch2:
        # print(switch1+" and "+switch2+" are the same switch.")
        return 1
    else:
        # print(switch1+" and "+switch2+" are different.")
        return 0

parser = argparse.ArgumentParser()
parser.add_argument("nodereq",help="Topology of requested nodes.",type=str)
args = parser.parse_args()
wanted_nodes = args.nodereq
wanted_nodes = wanted_nodes.split(",")
print("Wanted nodes: "+str(wanted_nodes))

free_node_list_backup = free_node_list
chosen_nodes = []
rack_representing_nodes = ["-1"] * len(wanted_nodes) # first node chosen for each rack
found1 = False
# iterate over all permunations of wanted_nodes elements in outer loop to eliminate chance of not finding solution because of search order
for wanted_nodes_permutation in itertools.permutations(wanted_nodes):
    print("Trying permutation "+str(wanted_nodes_permutation))
    rack = 0
    while rack < len(wanted_nodes):
        nodes_this_rack = []
        i_want_node=0
        free_node_list_backup1 = free_node_list
        start_with_i = 0
        # find nodes in the same rack
        while i_want_node < int(wanted_nodes[rack]):
            found1 = False
            i_check_node = start_with_i
            while i_check_node < len(free_node_list):
                if i_want_node == 0:
                    # check if the node is in a different rack than all in rack_representing_nodes
                    newRack = True
                    for inode_recheck_chosen in rack_representing_nodes:
                        if inode_recheck_chosen == "-1": 
                            break
                        same_rack = checkSameRack(inode_recheck_chosen,free_node_list[i_check_node])
                        if same_rack != 0: # same rack or not in topo file: skip node
                            newRack=False
                            break
                    if newRack is True:
                        nodes_this_rack.append(free_node_list[i_check_node])
                        del free_node_list[i_check_node]
                        found1 = True
                        break
                    else:
                        i_check_node = i_check_node+1
                else:
                    same_rack = checkSameRack(nodes_this_rack[i_want_node-1],free_node_list[i_check_node])
                    if same_rack == 1:
                        nodes_this_rack.append(free_node_list[i_check_node])
                        del free_node_list[i_check_node]
                        found1 = True
                        break
                    else:
                        i_check_node = i_check_node+1
                        continue
            # couldn't find enough nodes, start search with other node
            if not found1:
                i_want_node=0
                nodes_this_rack=[]
                free_node_list = free_node_list_backup1
                if start_with_i < len(free_node_list):
                    start_with_i = start_with_i+1
                else:
                    break
            else:
                i_want_node = i_want_node+1
        if found1:
            rack_representing_nodes[rack]=nodes_this_rack[0]
            for node_tr in nodes_this_rack:
                chosen_nodes.append(node_tr)
            rack += 1
        else: # couldn't find enough nodes in free nodes, try searching with another rack permutation
            free_node_list = free_node_list_backup
            rack_representing_nodes = []
            chosen_nodes = []
            print("Permutation unsuccessful.")
            break
    if found1:
        print("Search successful! Chosen nodes: "+str(chosen_nodes)+"\n")
        break
if not found1:
    print("Choosing nodes failed, rack requirements cannot be met with current idling nodes.")
    abort()

NODELIST = ",".join(chosen_nodes)

out_file.write("export NODELIST="+NODELIST+"\n")

out_file.write("export CHOOSE_NODES_FAILED=0\n")
topo_file.close()
out_file.close()