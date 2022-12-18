input_file = 'input.json'

import os
import json
import shutil
from contextlib import redirect_stdout

from drawtree import draw_level_order



# tree node definition
# two types of node: inner, leaf
class Node:
    def __init__(self, val):
        self.v = val
        self.leaf = False
        # inner: 
        self.l = None
        self.r = None
        self.l_cnt = 0
        self.r_cnt = 0
        # leaf: 
        self.c = []
        self.c_cnt = 0


# build recursively
# input: sorted integer list, level index, level_list
# output: root node, level_list (mut)
def build(key_list: list[int], level_idx: int, level_list: list[list[any]]):
    if not key_list:
        if len(level_list) <= level_idx:
            return None
        else:
            level_list[level_idx].append('#')
            return None
    
    # find median
    r_cnt = ( len(key_list) - 1 ) // 2
    l_cnt = ( len(key_list) - 1 ) - r_cnt
    median = key_list[l_cnt]
    
    # modify level list
    if len(level_list) <= level_idx:
        level_list.append([median])
    else:
        level_list[level_idx].append(median)
    
    # try create inner node
    node = Node(median)
    node.l = build(key_list[0:l_cnt], level_idx+1, level_list)
    node.r = build(key_list[l_cnt+1:], level_idx+1, level_list)
    node.l_cnt = l_cnt
    node.r_cnt = r_cnt
    
    # change into a leaf node if descendents < 4
    if (l_cnt + r_cnt) <= 4:
        node.leaf = True
        node.c.extend(key_list[0:l_cnt])
        node.c.extend(key_list[l_cnt+1:])
        node.c_cnt = l_cnt + r_cnt

    return node


# flatten list
# input: level list
# output: flattened list, flattened list as a string
def flatten_level_list(level_list: list[list[any]]):
    flattened_list = []
    
    for this_level in level_list:
        flattened_list.extend(this_level)

    list_string = '['
    for idx in range(0, len(flattened_list)):
        list_string += str(flattened_list[idx])
        if idx < len(flattened_list) - 1:
            list_string += ','
            
    list_string += ']'
    
    return flattened_list, list_string


# iterate and output minecraft file recursively
def output_file(node: Node):
    if not node:
        return
    
    # match self
    commands_to_run = input_dict[node.v]
    file_content = ''
    
    # # only one command to run
    if len(commands_to_run) < 2:
        cmd_to_run = commands_to_run[0]
        
        file_content += """execute if score {} matches {} run {}\n""" \
            .format(  obj_to_match, \
                      node.v, \
                      cmd_to_run)
    # # multiple commands, use a separate file
    else:
        file_to_run = str(node.v) + '_run.mcfunction'
        cmd_to_run = 'function ' + mcfunction_path + file_to_run
        
        file_content += """execute if score {} matches {} run {}\n""" \
            .format(  obj_to_match, \
                      node.v, \
                      cmd_to_run)
        
        with open(file_to_run, "w+") as f:
            content = ''
            for cmd in commands_to_run:
                content += cmd + '\n'
            f.write(content)
    
    # match children
    
    # # inner node
    if not node.leaf:
        # # # left
        if node.l:
            file_to_run = str(node.l.v) + '.mcfunction'
            cmd_to_run = 'function ' + mcfunction_path + file_to_run
            
            file_content += """execute if score {} matches ..{} run {}\n""" \
                .format(  obj_to_match, \
                          int(node.v) - 1,
                          cmd_to_run)
            
            output_file(node.l)
        
        # # # right
        if node.l:
            file_to_run = str(node.r.v) + '.mcfunction'
            cmd_to_run = 'function ' + mcfunction_path + file_to_run
            
            file_content += """execute if score {} matches {}.. run {}\n""" \
                .format(  obj_to_match, \
                          int(node.v) + 1,
                          cmd_to_run)
            
            output_file(node.r)
            
    # # leaf node
    else:
        for child in node.c:
            commands_to_run = input_dict[child]
            
            # # only one command to run
            if len(commands_to_run) < 2:
                cmd_to_run = commands_to_run[0]
                
                file_content += """execute if score {} matches {} run {}\n""" \
                    .format(  obj_to_match, \
                              child, \
                              cmd_to_run)
            # # multiple commands, use a separate file
            else:
                file_to_run = str(child) + '_run.mcfunction'
                cmd_to_run = 'function ' + mcfunction_path + file_to_run
                
                file_content += """execute if score {} matches {} run {}\n""" \
                    .format(  obj_to_match, \
                              child, \
                              cmd_to_run)
                
                with open(file_to_run, "w+") as f:
                    content = ''
                    for cmd in commands_to_run:
                        content += cmd + '\n'
                    f.write(content)
    
    # write to root node file
    file_name = str(node.v) + '.mcfunction'
    with open(file_name, "w+") as f:
        f.write(file_content)
    
    return



# main #

# read from a json file
with open(input_file) as f:
    input_file = json.load(f)

global input_dict
input_dict = input_file["data"]

global output_dir_path
global mcfunction_path
global obj_to_match
input_config = input_file["config"]
output_dir_path = input_config["output_dir_path"]
mcfunction_path = input_config["mcfunction_path"]
obj_to_match = input_config["obj_to_match"]

# sort keys
keys = list(input_dict.keys())
keys.sort()

# build tree and level list
level_list = []
root_node = build(keys, 0, level_list)

# draw tree
flattened_list, list_string = flatten_level_list(level_list)
with open('tree_graph.txt', 'w+') as f:
    with redirect_stdout(f):
        draw_level_order(list_string)

# output minecraft functions
if not os.path.isdir(output_dir_path):
    os.mkdir(output_dir_path)
os.chdir(output_dir_path)

output_file(root_node)