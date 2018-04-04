# generate the citation graph of the conf
# only consider the conf that SIGIR can reach within
# four citationd

import sys
import collections
import os
import json
import yaml

def get_index():
    global index_count
    tmp = index_count
    index_count += 1
    return tmp


def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

output_file = open("citation_network_input/largevis_input_file.txt", "w")
# output_file = open()
# input_dir = "/scratch/si699w18_fluxm/gaole"
input_dir_1 = "/scratch/si699w18_fluxm/gaole/aminer_papers_0"
input_dir_2 = "/scratch/si699w18_fluxm/gaole/aminer_papers_1"
input_dir_3 = "/scratch/si699w18_fluxm/gaole/aminer_papers_2"
input_dir_list = [input_dir_1, input_dir_2, input_dir_3]



conf_dict = {}
block_list = {}  # hold all the blocks data
possible_index = {}
id_to_json = {}
bfs_depth = 4
index_count = 0


for input_dir in input_dir_list:
    for filename in os.listdir(input_dir):
        file = open(os.path.join(input_dir, filename))
        for line in file:
            paper_json = yaml.load(json.dumps(json.loads(line)))
            id_to_json[paper_json["id"]] = paper_json
            if paper_json["venue"] not in conf_dict:
                conf_dict[paper_json["venue"]] = []
            if index_count == 0:
                print(paper_json)
                print(paper_json['venue'])
            conf_dict[paper_json["venue"]].append(paper_json["id"])
            index_count += 1
            sys.stdout.write("\r" + str(index_count))
        file.close()


print("finish")
print("SIGIR paper number: %s" % len(conf_dict["SIGIR"]))

conf_paper_counter = 0
for k, v in conf_dict.items():
    conf_paper_counter += len(v)
print("average number of paper per conf: %s" % str(float(conf_paper_counter) / len(conf_dict)))

deque = collections.deque(conf_dict["SIGIR"])

visited_conf = {}
visited = {}
for ele in deque:
    visited[ele] = 1

visited_conf["SIGIR"] = 1

for i in range(bfs_depth):
    next_deque = collections.deque([])
    while len(deque):
        next_paper = deque.pop()
        if next_paper not in id_to_json:
            continue
        citation_list = id_to_json[next_paper]["references"]
        for ele in citation_list:
            # output_file.write(str(next_paper) + " " + str(ele) + " " + "1\n")
            if ele in visited:
                continue
            next_deque.append(ele)
            visited[ele] = 1
            visited_conf[id_to_json[ele]["venue"]] = 1

    deque = next_deque


all_points_inconf = {}
for conf, v in visited_conf.items():
    for ele in conf_dict[conf]:
        all_points_inconf[ele] = 1

for conf, v in visited_conf.items():
    for ele in conf_dict[conf]:
        for v in id_to_json[ele]:
            if v in all_points_inconf:
                output_file.write(str(ele) + " " + str(v) + " 1\n")


conf_point_num = len(all_points_inconf) + 1
print("total vertices", len(visited))
for k, v in conf_dict.items():
    for index in v:
        output_file.write(str(conf_point_num) + " " + str(index) + " 1\n")
    conf_point_num += 1

# # for other in conf_dict[block.conf]:
# #     output_file.write(str(index) + " " + str(other) + " " + "1\n")

print("finish")
output_file.close()


