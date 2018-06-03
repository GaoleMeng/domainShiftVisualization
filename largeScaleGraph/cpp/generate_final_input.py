"""
the python version of "generate final input"
which takes the filtered file and output the edges computation
or it can read the final output of large vis and output the author point split
and paper embedding split
"""

import os
import sys
import json
import sets

# the 
input_dir_1 = "/home/wuzhuofeng/intermediate_files/lines_belong_toconf_smaller.txt";

output_file = "/home/wuzhuofeng/intermediate_files/non_bias_edges_withauthors.txt";

largeVis_output = "./citation_qiaozhu.txt";

split_location = "/home/wuzhuofeng/domainShiftVisualization/largeScaleGraph/cpp/final_visulization/";

conf_lines_file = open(input_dir_1)

conf_info = {}

index_count = 0

id_to_ref = {}
id_to_index = {}
year_to_indexlist = {}
year_counter = {}
author_to_index = {}
conf_pool = set()


def read_and_parse():
    global index_count
    for line in conf_lines_file:
        tmp_obj = json.loads(line)
        if "id" not in tmp_obj:
            continue
        if "venue" not in tmp_obj:
            continue
        if "year" not in tmp_obj:
            continue
        venue_list = tmp_obj["venue"]
        conf_pool.add(venue_list)

        id_string = tmp_obj["id"]
        year_string = tmp_obj["year"]
        if year_string not in year_to_indexlist:
            year_to_indexlist[year_string] = []

        id_to_index[id_string] = index_count

        if id_string not in id_to_ref:
            id_to_ref[id_string] = []

        if "authors" in tmp_obj:
            author_list = tmp_obj["authors"]
            for tmp in author_list:
                if "name" in tmp:
                    if tmp["name"] not in author_to_index:
                        author_to_index[tmp["name"]] = []
                    author_to_index[tmp["name"]].append(index_count)

        if "references" in tmp_obj:
            for ref in tmp_obj["references"]:
                for tmp in ref:
                    id_to_ref[id_string].append(tmp)

        year_to_indexlist[year_string].append(index_count)
        index_count += 1

def main():
    read_and_parse()
    
    


if __name__ == "__main__":
    main()


