"""
the python version of "generate final input"
which takes the filtered file and output the edges computation
or it can read the final output of large vis and output the author point split
and paper embedding split
"""

import os
import sys
import json

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


def read_and_parse():
    for line in conf_lines_file:
        tmp_obj = json.loads(line)
        if "id" not in tmp_obj:
            continue
        if "venue" not in tmp_obj:
            continue
        if "year" not in tmp_obj:
            continue
        venue_string = tmp_obj["venue"]
        id_string = tmp_obj["id"]
        author_list = tmp_obj["authors"]
        year_string = tmp_obj["year"]
        if year_string not in year_to_indexlist:
            year_to_indexlist[year_string] = []

        id_to_index[id_string] = index_count

        if id_string not in id_to_ref:
            id_to_ref[id_string] = []

        if "references" in tmp_obj:
            for ref in tmp_obj["references"]:
                for tmp in ref:
                    id_to_index[id_string].append(tmp)
        
        year_to_indexlist[year_string].append(index_count)
        index_count += 1

def main():
    read_and_parse()
    
    


if __name__ == "__main__":
    main()


