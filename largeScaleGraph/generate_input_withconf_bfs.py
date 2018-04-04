# generate the input edges to the large vis
# link generated between same conf/ citation
# output all the node with reference recorded

#*Real-Time and Embedded Systems.
#@John A. Stankovic
#t1997
#cThe Computer Science and Engineering Handbook
#index395
#%808022
#%1071742
#%3003326
#!
import sys
import collections

output_file = open("citation_network_input/citation_conf_edge_bfs_v7.txt", "w")
f = open("publications.txt")

conf_dict = {}
block_list = {}  # hold all the blocks data
possible_index = {}
bfs_depth = 4


class Block(object):
    def __init__(self, index, conf, citelist):
        self.index = index
        self.conf = conf
        self.citation = citelist

iii = 0
max_index = 0

while(True):
    index = -1
    conf = ""
    year = ""
    # print(i)
    line = f.readline().strip()
    # print(iii)
    if line == "":
        break
    flag = True
    citation = []
    sys.stdout.write("\r" + str(iii))
    while(True):
        if len(line) >= 6 and line[0:6] == "#index":
            line = line[6:]
            index = int(line)
            possible_index[index] = 1
            conf_dict[conf].append(index)
            block_list[index] = Block(index, conf, citation)
            max_index = max(int(index), max_index)
        elif len(line) == 0:
            iii += 1
            conflist = []
            break
        elif len(line) >= 3 and line[0:2] == "#c":
            line = line[2:].strip()
            conf = line
            if conf not in conf_dict:
                conf_dict[conf] = []
        elif len(line) >= 3 and line[0:2] == "#%":
            line = line[2:].strip()
            citation.append(int(line))
            max_index = max(max_index, int(line))
        # elif len(line) >= 3 and line[0:2] == "#t":
        #     line = line[2:].strip()
        #     year = line
        #     if year not in possible_year_map:
        #         possible_year_map[year] = []
        line = f.readline().strip()

f.close()
print("finish")
print("SIGIR paper number: %s" % len(conf_dict["SIGIR"]))

conf_paper_counter = 0
for k, v in conf_dict.items():
    conf_paper_counter += len(v)
print("average number of paper per conf: %s" % str(float(conf_paper_counter) / len(conf_dict)))

deque = collections.deque(conf_dict["SIGIR"])
visited = {}
for ele in deque:
    visited[ele] = 1

for i in range(bfs_depth):
    next_deque = collections.deque([])
    while len(deque):
        next_paper = deque.pop()
        if next_paper not in block_list:
            continue
        citation_list = block_list[next_paper].citation
        for ele in citation_list:
            output_file.write(str(next_paper) + " " + str(ele) + " " + "1\n")
            if ele in visited:
                continue
            next_deque.append(ele)
            visited[ele] = 1
    deque = next_deque

conf_point_num = len(visited) + 1
print("total vertices", len(visited))
for k, v in conf_dict.items():
    for index in v:
        if index not in visited:
            continue
        output_file.write(str(conf_point_num) + " " + str(index) + " 1\n")
    conf_point_num += 1

# # for other in conf_dict[block.conf]:
# #     output_file.write(str(index) + " " + str(other) + " " + "1\n")

print("finish")
output_file.close()


