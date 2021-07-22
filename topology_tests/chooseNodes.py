#!/usr/bin/python

import os
import re
import numpy as np
import argparse

path_to_script = os.path.dirname(os.path.abspath(__file__))
out_path = path_to_script + "/chosenNodes.sh"
out_file = open(out_path, 'w')

def abort():
    out_file.write("export CHOOSE_NODES_FAILED=1\n")
    out_file.close()
    os._exit(1)

#########################################################
#              Get and parse idle nodes                 #
#########################################################
fake_input = "c18m         up 30-00:00:0    243   idle ncm[0003,0005,0008,0030,0038,0074-0075,0079,0110,0114,0116-0119,0121-0123,0126,0128-0130,0133-0134,0138,0142-0143,0145,0202-0203,0218,0238-0248,0250-0251,0254-0256,0259,0332-0333,0344-0349,0473-0477,0479-0494,0497-0504,0571,0573-0575,0585-0587,0591-0598,0601,0603-0614,0616,0646,0677,0686,0690,0693-0694,0696-0700,0702-0706,0708,0714,0716,0815-0819,0822-0832,0863-0864,0877-0879,0881-0890,0892-0903,0930-0936,0938],nrm[027-035,037,041-052,069-071,112-113,115-130,132-144,175-176,180,195] \n c18m_low     up 30-00:00:0    243   idle ncm[0003,0005,0008,0030,0038,0074-0075,0079,0110,0114,0116-0119,0121-0123,0126,0128-0130,0133-0134,0138,0142-0143,0145,0202-0203,0218,0238-0248,0250-0251,0254-0256,0259,0332-0333,0344-0349,0473-0477,0479-0494,0497-0504,0571,0573-0575,0585-0587,0591-0598,0601,0603-0614,0616,0646,0677,0686,0690,0693-0694,0696-0700,0702-0706,0708,0714,0716,0815-0819,0822-0832,0863-0864,0877-0879,0881-0890,0892-0903,0930-0936,0938],nrm[027-035,037,041-052,069-071,112-113,115-130,132-144,175-176,180,195]"
free_nodes = fake_input

# free_nodes = os.popen('sinfo | grep c18m | grep idle').read()
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
    print(free_nodes[i])
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

print(free_node_list)

#########################################################
#                   Choose nodes                        #
#########################################################
def checkSameRack(node1, node2):
    # TODO: check if node1 and node2 are on the same rack (have the same leaf switch)
    return True

parser = argparse.ArgumentParser()
parser.add_argument("nodereq",help="Topology of requested nodes.",type=str)
args = parser.parse_args()
wanted_nodes = args.nodereq
wanted_nodes = wanted_nodes.split(",")
print(wanted_nodes)
topo_path = path_to_script + "/mapping_switches_nodes.log"
topo_file = open(out_path, 'r')

free_node_list_backup = free_node_list
chosen_nodes = []
rack_representing_nodes = [] # first node chosen for each rack
# TODO: reset rack search one step when inner search fails completely
for rack in range(len(wanted_nodes)):
    nodes_this_rack = []
    i_want_node=0
    free_node_list_backup1 = free_node_list
    start_with_i = 0
    while i_want_node < range(int(wanted_nodes[rack])):
        found1 = False
        i_check_node = start_with_i
        while i_check_node < len(free_node_list):
            if i_want_node == 0:
                # TODO: check if the node is in a different rack than all in rack_representing_nodes
                nodes_this_rack.append(free_node_list[i_check_node])
                del free_node_list[i_check_node]
                found1 = True
                break
            else:
                if checkSameRack(nodes_this_rack[i_want_node-1],free_node_list[i_check_node]):
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
            i_want_node = i_want_node+1
    if found1:
        rack_representing_nodes[rack]=nodes_this_rack[0]



# out_file.write("export FREE_NODES="+str(chosen_nodes))

out_file.write("export CHOOSE_NODES_FAILED=0\n")
topo_file.close()
out_file.close()