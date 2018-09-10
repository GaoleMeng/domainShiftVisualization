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
input_dir_1 = "/home/zhuofeng/lines_belong_toconf_smaller.txt";

output_file = "/home/zhuofeng/non_bias_edges_withauthors.txt";

largeVis_output = "./citation_qiaozhu.txt";

split_location = "./final_visulization/";

class_map_file = "./class_map.txt"


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

        if "keywords" in tmp_obj:
            for keyword in tmp_obj["keywords"]:
                keywords_pool.add(keyword)

        if id_string not in id_to_ref:
            id_to_ref[index_count] = []

        if venue_string == "SIGIR" or venue_string == "SIGIR Forum":
            if year_string not in year_counter:
                year_counter[year_string] = 0
            year_counter[year_string] += 1
            sigir_pool.add(index_count)
            tmp_counter += 1

            if year_string == "2015":
                counter_15 += 1

        if "authors" in tmp_obj:
            author_list = tmp_obj["authors"]
            for tmp in author_list:
                print(tmp)
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



def generate_index_to_loc():
    tmp_file = open(largeVis_output)
    outfile = open("./title_loc.txt", "w")
    for line in tmp_file:
        vec = line.split()
        index_to_loc[vec[0]] = line
        if vec[0] in index_to_title:
            outfile.write(index_to_title[vec[0]] + "\t" + vec[1] + "\t" + vec[2] + "\n")

    # print(index_to_loc)

    outfile.close()
    tmp_file.close()


def generate_conf_index():
    global index_count
    for conf in conf_pool:
        conf_to_index[conf] = index_count
        # print(conf)
        if conf + "\n" in eq_name_map:
            eq_name_to_index[conf] = index_count
        elif conf == "SIGMOD Conference":
            eq_name_to_index[conf] = index_count
        index_count += 1

    # for k, v in sorted(conf_count.items(), key=lambda x:x[1]):
    #     print("%s %s" % (k, v))

    # print("total conf number: ", len(conf_pool))


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


def generate_files():
    year_counter_list = sorted(year_counter.items(), key=lambda x:x[0])
    # print(year_counter_list)
    # print(tmp_counter)
    cur_layer = 1
    layer_list = {}
    for k, v in sorted(year_to_indexlist.items(), key=lambda x:x[0]):
        if cur_layer not in layer_list:
            layer_list[cur_layer] = []
        for tmp in v:
            # if str(tmp) not in index_to_loc:
            #     continue
            layer_list[cur_layer].append(tmp)
        # print(k)
        if str(k) in split_points:
            cur_layer += 1
    # print(len(layer_list))

    tmp_counter = 0
    for k, v in sorted(layer_list.items(), key=lambda x:x[0]):
        point_file = open(split_location + str(k) + "_points.txt", 'w')
        label_file = open(split_location + str(k) + "_labels.txt", 'w')

        # point_file.write(str(len(v)) + "\n")
        point_list = []
        label_list = []
        for tmp in v:
            conf = index_to_conf[tmp]

            # if conf == "SIGIR Forum":
            #     point_list.append(index_to_loc[str(tmp)])
            #     label_list.append("1\n")

            if conf in color_map:
                if conf == "SIGIR" or conf == "SIGIR Forum":
                    tmp_counter += 1
                point_list.append(index_to_loc[str(tmp)])
                label_list.append("%s\n" % color_map[conf])
                # point_file.write(index_to_loc[str(tmp)])
                # label_file.write("%s\n" % color_map[conf])

        point_file.write(str(len(point_list)) + "\n")

        for tmp in range(len(point_list)):
            point_file.write(point_list[tmp])
            label_file.write(label_list[tmp])

        point_file.close()
        label_file.close()

    print("sigir input ", tmp_counter)
    # print(len(author_to_self_index))
    # print(keywords_pool)
    # print(len(keywords_pool))
    for i in range(3):
        author_file = open(split_location + str(i) + "_authors.txt", "w")

        tmp_list = []
        for k, author_dict in author_to_index.items():
            elementX = 0.0
            elementY = 0.0
            counter = 0
            # print(k, author_dict)

            for k, v in author_dict.items():
                if str(k) > split_points[i] and str(k) < split_points[i+1]:
                    for index in v:
                        if str(index) not in index_to_loc:
                            continue
                        vec = index_to_loc[str(index)].strip().split()
                        elementX += float(vec[1])
                        elementY += float(vec[2])
                        counter += 1.0
            if counter != 0:
                tmp_list.append("1 %s %s\n" % (elementX / counter, elementY / counter))

        author_file.write(str(len(tmp_list)) + "\n")
        for tmp in tmp_list:
            author_file.write(tmp)

        author_file.close()

    print("find eq_name: ", len(eq_name_to_index))
    for conf in eq_name_to_index.keys():
        print(conf, index_to_loc[str(eq_name_to_index[conf])].strip())
        # eq_name_to_index




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
    generate_conf_index()
    generate_edges()
    generate_index_to_loc()
    generate_files()





if __name__ == "__main__":

    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()

