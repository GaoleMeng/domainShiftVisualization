"""
the python version of "generate final input"
which takes the filtered file and output the edges computation
or it can read the final output of large vis and output the author point split
and paper embedding split
"""

import os
import sys
import json
import csv




# the
input_dir_1 = "/home/wuzhuofeng/intermediate_files/lines_belong_toconf_smaller.txt";

output_file = "/home/wuzhuofeng/intermediate_files/non_bias_edges_withauthors.txt";

largeVis_output = "./citation_qiaozhu.txt";

split_location = "/home/wuzhuofeng/domainShiftVisualization/largeScaleGraph/cpp/final_visulization/";

class_map_file = "./class_map.txt"


conf_info = {}

index_count = 0

id_to_ref = {}
id_to_index = {}
year_to_indexlist = {}
year_counter = {}   # count the sigir paper in each year
author_to_index = {}
conf_to_index = {}
index_to_conf = {}
index_to_loc = {}
index_to_title = {}


tmp_counter = 0
author_to_self_index = {}
conf_count = {}

split_points = ['0000', '1997', '2008', '3000']

color_map = {}
eq_name_map = {}
eq_name_to_index = {}

counter_15 = {};


def read_and_parse():
    global index_count
    global tmp_counter
    global counter_15
    conf_lines_file = open(input_dir_1)
    for line in conf_lines_file:
        tmp_obj = json.loads(line)
        if "id" not in tmp_obj:
            continue
        if "venue" not in tmp_obj:
            continue
        if "year" not in tmp_obj:
            continue
        venue_string = tmp_obj["venue"]
        # conf_pool.add(venue_string)
        if venue_string not in conf_count:
            conf_count[venue_string] = 0
        conf_count[venue_string] += 1


        id_string = tmp_obj["id"]
        year_string = tmp_obj["year"]
        if year_string not in year_to_indexlist:
            year_to_indexlist[year_string] = []

        id_to_index[id_string] = index_count
        index_to_conf[index_count] = venue_string

        # if venue_string not in conf_to_index:
        #     conf_to_index[venue_string] = []
        # conf_to_index.append(index_count)

        # if "keywords" in tmp_obj:
        #     for keyword in tmp_obj["keywords"]:
        #         # keywords_pool.add(keyword)

        if id_string not in id_to_ref:
            id_to_ref[index_count] = []

        if "SIGIR" in venue_string or "sigir" in venue_string:
            if year_string not in counter_15:
                counter_15[year_string] = 0
            counter_15[year_string] += 1

        # if venue_string == "SIGIR" or venue_string == "SIGIR Forum":
        #     if year_string not in year_counter:
        #         year_counter[year_string] = 0
        #     year_counter[year_string] += 1
        #     # sigir_pool.add(index_count)
        #     tmp_counter += 1

        #     # print(year_string)
        #     if year_string not in counter_15:
        #         counter_15[year_string] = 0
        #     counter_15[year_string] += 1

        if "authors" in tmp_obj:
            author_list = tmp_obj["authors"]
            for tmp in author_list:
                if "name" in tmp:
                    if tmp["name"] not in author_to_index:
                        author_to_index[tmp["name"]] = {}
                    if year_string not in author_to_index[tmp["name"]]:
                        author_to_index[tmp["name"]][year_string] = []
                    author_to_index[tmp["name"]][year_string].append(index_count)

                    if tmp["name"] not in author_to_self_index:
                        author_to_self_index[tmp["name"]] = len(author_to_self_index)

                    # author_to_index[tmp["name"]].append(index_count)

        index_to_title[str(index_count)] = tmp_obj["title"]

        if "references" in tmp_obj:
            for ref in tmp_obj["references"]:
                id_to_ref[index_count].append(ref)

        year_to_indexlist[year_string].append(index_count)
        index_count += 1
    conf_lines_file.close()





def create_class_map():
    class_file = open(class_map_file)
    all_conf = []
    tmp_conf = ""
    for line in class_file:
        vec = line.split("\t")
        conf_name = vec[2][0: vec[2].rfind(" ")]
        eq_name = vec[3]
        all_conf.append([conf_name, eq_name])
        if eq_name not in eq_name_map:
            eq_name_map[eq_name] = len(eq_name_map)
            if eq_name_map[eq_name] == 7:
                tmp_conf = eq_name

    print(eq_name_map)
    # tmp = eq_name_map["SIGIR\n"]
    # eq_name_map["SIGIR\n"] = 7
    # eq_name_map[tmp_conf] = tmp

    for k, v in all_conf:
        color_map[k] = eq_name_map[v]

    # print(color_map)
    # print(eq_name_map)
    print("unique conf:" + str(len(eq_name_map)))
    class_file.close()




def main():

    create_class_map()
    read_and_parse()
    print(counter_15)
    for k, v in sorted(counter_15.items(), key=lambda x:x[0]):
        print(k, v)



if __name__ == "__main__":

    # reload(sys)
    # sys.setdefaultencoding('utf-8')
    main()

