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




def read_and_parse():
    for line in conf_lines_file:
        tmp_obj = json.loads(line)
        print(tmp_obj["id"])
        break
         


def main():
    read_and_parse()
    
    


if __name__ == "__main__":
    main()


