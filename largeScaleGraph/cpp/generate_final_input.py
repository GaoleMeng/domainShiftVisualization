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
import csv




# the
input_dir_1 = "/storage6/foreseer/users/zhuofeng/visualization_of_conference_evolution/tmp_files/lines_belong_toconf_smaller.txt";

output_file = "/storage6/foreseer/users/zhuofeng/visualization_of_conference_evolution/tmp_files/non_bias_edges_withauthors.txt";

largeVis_output = "./citation_qiaozhu.txt";

split_location = "./final_visulization/";

# class_map_file = "./class_map.txt"


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
index_to_loc = {}
index_to_title = {}
index_to_year = {}
conf_index_pool = {}


tmp_counter = 0
author_to_self_index = {}
keywords_pool = set()
conf_count = {}

split_points = ['0000', '1997', '2008', '3000']

color_map = {}
eq_name_map = {}
eq_name_to_index = {}

counter_15 = 0;


def read_and_parse():
    global index_count
    global tmp_counter
    global counter_15
    conf_lines_file = open(input_dir_1)

    # we need title,x,y,venue,index,label,year
    for line in conf_lines_file:
        tmp_obj = json.loads(line)
        if "id" not in tmp_obj:
            continue
        if "venue" not in tmp_obj:
            continue
        if "year" not in tmp_obj:
            continue
        if "title" not in tmp_obj:
            continue
        if "year" not in tmp_obj:
            continue

        venue_string = tmp_obj["venue"]
        title_string = tmp_obj["title"]
        
        conf_pool.add(venue_string)
        if venue_string not in conf_count:
            conf_count[venue_string] = 0
        conf_count[venue_string] += 1

        id_string = tmp_obj["id"]
        year_string = tmp_obj["year"]
        if year_string not in year_to_indexlist:
            year_to_indexlist[year_string] = []

        id_to_index[id_string] = index_count
        index_to_conf[index_count] = venue_string
        index_to_title[index_count] = title_string
        index_to_year[index_count] = tmp_obj["year"]

        if "keywords" in tmp_obj:
            for keyword in tmp_obj["keywords"]:
                keywords_pool.add(keyword)

        if id_string not in id_to_ref:
            id_to_ref[index_count] = []

        if "authors" in tmp_obj:
            author_list = tmp_obj["authors"]
            for tmp in author_list:
                tmp = tmp.encode("utf-8")
                if tmp not in author_to_index:
                    author_to_index[tmp] = {}
                if year_string not in author_to_index[tmp]:
                    author_to_index[tmp][year_string] = []
                author_to_index[tmp][year_string].append(index_count)

                if tmp not in author_to_self_index:
                    author_to_self_index[tmp] = len(author_to_self_index)

        index_to_title[str(index_count)] = tmp_obj["title"]

        if "references" in tmp_obj:
            for ref in tmp_obj["references"]:
                id_to_ref[index_count].append(ref)

        year_to_indexlist[year_string].append(index_count)
        index_count += 1
    conf_lines_file.close()
    print("number of conferences: ", len(conf_pool))



def generate_index_to_loc():
    tmp_file = open(largeVis_output)
    outfile = open("./new/title_2dim_with_index_year_venue.csv", "w")
    conf_info_outfile = open("./new/conf_info.csv", "w")
    fieldnames = ["title", "x", "y", "venue", "index", "label", "year"]
    conf_fieldnames = ["conf_name", "x", "y", "label"]

    writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=",")
    writer.writeheader()

    conf_writer = csv.DictWriter(conf_info_outfile, fieldnames=conf_fieldnames, delimiter=",")
    conf_writer.writeheader()

    counter = 0
    
    # we need title,x,y,venue,index,label,year
    for line in tmp_file:
        if counter == 0:
            counter = 1
            continue
        vec = line.split()
    
        if int(vec[0]) in conf_index_pool:
            tmp_obj = {}
            tmp_obj["conf_name"] = conf_index_pool[int(vec[0])]
            tmp_obj["x"] = vec[1]
            tmp_obj["y"] = vec[2]
            tmp_obj["label"] = vec[0]
            conf_writer.writerow(tmp_obj)
        else:
            index_to_loc[vec[0]] = line
            tmp_row = {}
            tmp_row["x"] = vec[1]
            tmp_row["y"] = vec[2]
            tmp_row["title"] = index_to_title[int(vec[0])]
            tmp_row["venue"] = index_to_conf[int(vec[0])]
            tmp_row["year"] = index_to_year[int(vec[0])]
            tmp_row["label"] = conf_to_index[index_to_conf[int(vec[0])]]
            tmp_row["index"] = vec[0]
            writer.writerow(tmp_row)

    # print(index_to_loc)
    outfile.close()
    conf_info_outfile.close()
    tmp_file.close()


def generate_conf_index():
    global index_count
    for conf in conf_pool:
        conf_to_index[conf] = index_count
        conf_index_pool[index_count] = conf
        # print(conf)
        # if conf + "\n" in eq_name_map:
        #     eq_name_to_index[conf] = index_count
        # elif conf == "SIGMOD Conference":
        #     eq_name_to_index[conf] = index_count
        index_count += 1
    # index_count = 0


def generate_edges():
    out_edges_file = open(output_file, "w")
    for k, v in id_to_ref.items():
        for tmp in v:
            if tmp not in id_to_index:
                continue
            out_edges_file.write(str(k) + " " + str(id_to_index[tmp]) + " 1\n")

    tmp_counter = 0
    for k, v in index_to_conf.items():
        out_edges_file.write(str(k) + " " + str(conf_to_index[v]) + " 1\n");
        if v == "SIGIR" or v == "SIGIR Forum":
            tmp_counter += 1
    print("the paper in sigir:", tmp_counter)
    out_edges_file.close()


# def create_class_map():
#     class_file = open(class_map_file)
#     all_conf = []
#     tmp_conf = ""
#     for line in class_file:
#         vec = line.split("\t")
#         conf_name = vec[2][0: vec[2].rfind(" ")]
#         eq_name = vec[3]
#         all_conf.append([conf_name, eq_name])
#         if eq_name not in eq_name_map:
#             eq_name_map[eq_name] = len(eq_name_map)
#             if eq_name_map[eq_name] == 7:
#                 tmp_conf = eq_name

#     print(eq_name_map)
#     # tmp = eq_name_map["SIGIR\n"]
#     # eq_name_map["SIGIR\n"] = 7
#     # eq_name_map[tmp_conf] = tmp

#     for k, v in all_conf:
#         color_map[k] = eq_name_map[v]

#     # print(color_map)
#     # print(eq_name_map)
#     print("unique conf:" + str(len(eq_name_map)))
#     class_file.close()




def main():
    # create_class_map()
    
    read_and_parse()
    generate_conf_index()
    generate_edges()
    generate_index_to_loc()
    # generate_files()





if __name__ == "__main__":

    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()

