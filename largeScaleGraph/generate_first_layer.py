# generate the citation graph of the conf
# only consider the conf that SIGIR can reach within
# four citationd

import sys
import collections
import os
import json
import yaml
import gc

def get_index():
    global index_count
    tmp = index_count
    index_count += 1
    return tmp

output_file = open("/scratch/si699w18_fluxm/gaole/round_0.txt", "w")
# output_file = open()
# input_dir = "/scratch/si699w18_fluxm/gaole"
input_dir_1 = "/scratch/si699w18_fluxm/gaole/aminer_papers_0"
input_dir_2 = "/scratch/si699w18_fluxm/gaole/aminer_papers_1"
input_dir_3 = "/scratch/si699w18_fluxm/gaole/aminer_papers_2"
input_dir_list = [input_dir_1, input_dir_2, input_dir_3]

block_list = {}  # hold all the blocks data
possible_index = {}
id_to_json = {}
id_to_index = {}

bfs_depth = 4
index_count = 0


for input_dir in input_dir_list:
    for filename in os.listdir(input_dir):
        file = open(os.path.join(input_dir, filename))
        for line in file:
            paper_json = yaml.load(json.dumps(json.loads(line)))
            if "venue" not in paper_json:
                continue
            if paper_json["venue"] != "SIGIR":
                continue
                print("ddd")
            conf_str = ""
            for paper in paper_json["references"]:
                conf_str += paper
                conf_str += " "
            output_file.write("%s %s %s\n" % (paper_json["id"], "SIGIR", conf_str))

            index_count += 1
            sys.stdout.write("\r" + str(index_count))

        file.close()

print("finish")
output_file.close()


