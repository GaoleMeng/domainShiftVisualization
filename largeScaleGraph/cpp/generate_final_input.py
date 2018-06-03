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
year_counter = {}   # count the sigir paper in each year
author_to_index = {}
conf_pool = set()
sigir_pool = set()
conf_to_index = {}
index_to_conf = {}


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
        venue_string = tmp_obj["venue"]
        conf_pool.add(venue_string)
        id_string = tmp_obj["id"]
        year_string = tmp_obj["year"]
        if year_string not in year_to_indexlist:
            year_to_indexlist[year_string] = []

        id_to_index[id_string] = index_count
        index_to_conf[index_count] = venue_string

        # if venue_string not in conf_to_index:
        #     conf_to_index[venue_string] = []
        # conf_to_index.append(index_count)

        if id_string not in id_to_ref:
            id_to_ref[index_count] = []

        if venue_string == "SIGIR" or venue_string == "SIGIR Forum":
            if year_string not in year_counter:
                year_counter[year_string] = 0
            year_counter[year_string] += 1

        if "authors" in tmp_obj:
            author_list = tmp_obj["authors"]
            for tmp in author_list:
                if "name" in tmp:
                    if tmp["name"] not in author_to_index:
                        author_to_index[tmp["name"]] = []
                    author_to_index[tmp["name"]].append(index_count)

        if "references" in tmp_obj:
            for ref in tmp_obj["references"]:
                id_to_ref[index_count].append(ref)

        year_to_indexlist[year_string].append(index_count)
        index_count += 1


def generate_conf_index():
    global index_count
    for conf in conf_pool:
        conf_to_index[conf] = index_count
        index_count += 1


def generate_edges():
    out_edges_file = open(output_file, "w")
    for k, v in id_to_ref.items():
        for tmp in v:
            if tmp not in id_to_index:
                continue
            out_edges_file.write(str(k) + " " + str(id_to_index[tmp]) + " 1\n")
    for k, v in index_to_conf.items():
        out_edges_file.write(str(k) + " " + str(conf_to_index[v]) + " 2\n");



def main():
    read_and_parse()
    generate_conf_index()
    generate_edges()
    
    


if __name__ == "__main__":
    main()


