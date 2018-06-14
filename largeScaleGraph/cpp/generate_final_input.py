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

tmp_counter = 0
author_to_self_index = {}
keywords_pool = set()
conf_count = {}

split_points = ['0000', '1997', '2008', '3000']

color_map = {}
eq_name_map = {}
eq_name_to_index = {}


# color_map = {
#     "Commun. ACM": 1,
#     "NIPS": 2,
#     "CHI": 3,
#     "SIGIR": 4,
#     "CIKM": 5,
#     "ICDE": 6,
#     "ACL": 7,
#     "ACM Multimedia": 8, #MM
#     "SIGMOD Conference": 9,
#     "JASIST": 10,
#     "COLING": 11,
#     "STOC": 12,
#     "KDD": 13,
#     "VLDB": 14,
#     "JASIS": 15,
#     "WWW": 16,
#     "ICDM": 17,
#     "TREC": 18,
#     "CLEF (Working Notes)": 19, # CLEF
#     "JCDL": 20,
#     "UAI": 21,
#     "CSCW": 22,
#     "EMNLP": 23,
#     "HLT-NAACL": 24,
#     "IUI": 25,
#     "SDM": 26,
#     "DASFAA": 27,
#     "EDBT": 28,
#     "ECIR": 29,
#     "COLT": 30,
#     "SSDBM": 31,
#     "AAAI/IAAI": 32, # AAAI
#     "ICWSM": 33,
#     "EACL": 34,
#     "PODS": 35,
#     "RecSys": 36,
#     "CVPR (1)": 37, # CVPR
#     "VLDB J.": 38, 
#     "CVPR (2)": 37,
#     "meeting of the association for computational linguistics": 7, # ACL
#     "WSDM": 40,
#     "CLEF": 19,
#     "AIRS": 42,
#     "SOSP": 43,
#     "Journal of The American Society for Information Science and Technology": 10, # JASIST
#     "uncertainty in artificial intelligence": 21, # UAI
#     "International Conference on Machine Learning": 46, # ICML
#     "World Wide Web Conference Series": 16, # WWW
#     "Multimedia Information Retrieval": 48,
#     "COLING (Posters)": 49, # COLING
#     "International Joint Conference on Artificial Intelligence": 50, # IJCAI
#     "HLT": 24, # HLT-NAACL
#     "Neural Information Processing Systems": 2,
#     "WWW Posters": 16, # WWW
#     "EMNLP-CoNLL": 23, # EMNLP
#     "ACL (Short Papers)": 7, # ACL
#     "International Conference on Information and Knowledge Management": 5, # CIKM
#     "Meeting of the Association for Computational Linguistics": 7, # ACL
#     "COLING-ACL": 7, # ACL
#     "Conference on Computer Supported Cooperative Work": 22, # CSCW
#     "International Conference on Data Engineering": 6, # ICDE
#     "WWW (Special interest tracks and posters)": 16, # WWW
#     "Very Large Data Bases": 14, # VLDB
#     "WWW (Alternate Track Papers & Posters)": 16, # WWW
#     "IJCAI (1)": 50, # IJCAI
#     "HLT/EMNLP": 23, # EMNLP
#     "Text REtrieval Conference": 18, # TREC
#     "international world wide web conferences": 16, # WWW
#     "HLT-NAACL (Short Papers)": 24, # HLT-NAACL
#     "Conference of the European Chapter of the Association for Computational Linguistics": 34, # EACL
#     "ACL/IJCNLP": 7, # ACL
#     "ACM/IEEE Joint Conference on Digital Libraries": 20, # JCDL
#     "HLT '89 Proceedings of the workshop on Speech and Natural Language": 24, # HLT-NAACL
#     "CLEF (Notebook Papers/LABs/Workshops)": 19, # CLEF
#     "Research and Development in Information Retrieval": 4, # SIGIR
#     "conference on information and knowledge management": 5, # CIKM
#     "Digital Libraries": 20, # JCDL
#     "HLT '91 Proceedings of the workshop on Speech and Natural Language": 24, # HLT-NAACL
#     "Uncertainty in Artificial Intelligence": 21, # UAI
#     "Knowledge Discovery and Data Mining": 13, # KDD
#     "north american chapter of the association for computational linguistics": 24, # HLT-NAACL
#     "ACL/IJCNLP (Short Papers)": 7, # ACL
#     "NAACL": 24, # HLT-NAACL
#     "Cross-Language Evaluation Forum": 19, # CLEF
#     "Intelligent User Interfaces": 25, # 
#     "North American Chapter of the Association for Computational Linguistics": 24, # HLT-NAACL
#     "HLT '02 Proceedings of the second international conference on Human Language Technology Research": 24, # HLT-NAACL
#     "conference on computer supported cooperative work": 22, # CSCW
#     "HLT '93 Proceedings of the workshop on Human Language Technology": 24, # HLT-NAACL
#     "International Conference on Computer Vision": 51, # ICCV
#     "HLT '01 Proceedings of the first international conference on Human language technology research": 24, # HLT-NAACL
#     "CHI '82 Proceedings of the 1982 Conference on Human Factors in Computing Systems": 3, # CHI
#     "Journal of the American Society for Information Science": 15, # JASIS
#     "IEEE International Conference on Data Mining": 17, # ICDM
#     "CHI '83 Proceedings of the SIGCHI Conference on Human Factors in Computing Systems": 3, # CHI
#     "knowledge discovery and data mining": 13, # KDD
#     "ACM Multimedia": 8, # MM
#     "ACM Multimedia (1)": 8, # MM
#     "CHI '87 Proceedings of the SIGCHI/GI Conference on Human Factors in Computing Systems and Graphics Interface": 3, # CHI
#     "Conference on Information and Knowledge Management": 5, # CIKM
#     "CHI '86 Proceedings of the SIGCHI Conference on Human Factors in Computing Systems": 3, # CHI
#     "International Conference on Database Theory": 52, # ICDT
#     "CHI '88 Proceedings of the SIGCHI Conference on Human Factors in Computing Systems": 3, # CHI
#     "CLEF (1)": 19, # CLEF
#     "Digital Libraries'99": 20, # JCDL
#     "HLT-NAACL-Short '04 Proceedings of HLT-NAACL 2004: Short Papers": 24, # HLT-NAACL
#     "TREC Video Retrieval Evaluation": 18, # TREC
#     "international acm sigir conference on research and development in information retrieval": 4, # SIGIR
#     "EMNLP '02 Proceedings of the ACL-02 conference on Empirical methods in natural language processing - Volume 10": 23, # EMNLP
#     "KDD Cup": 13, # KDD
#     "Empirical Methods in Natural Language Processing": 23, # EMNLP
#     "KDD Workshop": 13, "KDD"
#     "CSLDAMT '10 Proceedings of the NAACL HLT 2010 Workshop on Creating Speech and Language Data with Amazon's Mechanical Turk": 24, # HLT-NAACL
#     "SIGMOD '12 Proceedings of the 2012 ACM SIGMOD International Conference on Management of Data": 9, # SIGMOD
#     "CLEF (2)": 19, # CLEF
#     "ACLdemo '04 Proceedings of the ACL 2004 on Interactive poster and demonstration sessions": 7, # ACL
#     "SIGMOD Workshop, Vol. 2": 9, # SIGMOD
#     "empirical methods in natural language processing": 23, # EMNLP
#     "CHI '85 Proceedings of the SIGCHI Conference on Human Factors in Computing Systems": 3, # CHI
#     "EMNLP '03 Proceedings of the 2003 conference on Empirical methods in natural language processing": 23, # EMNLP
#     "MULTIMEDIA '96 Proceedings of the fourth ACM international conference on Multimedia": 8, # MM
#     "EMNLP '00 Proceedings of the 2000 Joint SIGDAT conference on Empirical methods in natural language processing and very large corpora: held in conjunction with the 38th Annual Meeting of the Association for Computational Linguistics - Volume 13": 23, # EMNLP
#     "very large data bases": 14, # VLDB
#     "Human Language Technology": 53, # HLT/NAACL
#     "international conference on weblogs and social media": 33, # ICWSM
#     "ACM Multimedia EMME Workshop": 8, # MM
#     "KDD Workshop on Human Computation": 13, # KDD
#     "european conference on information retrieval": 29, # ECIR
#     "CIKM-iNEWS": 5, # CIKM
#     "ICCV '98 Proceedings of the Sixth International Conference on Computer Vision": 51, # ICCV
#     "COLING '69 Proceedings of the 1969 conference on Computational linguistics": 11, # COLING
#     "Proceedings of the 22nd annual international ACM SIGIR conference on Research and development in information retrieval": 4, # SIGIR
#     "SNA@ICML": 46, # ICML
#     "HLT-NAACL-LWM '04 Proceedings of the HLT-NAACL 2003 workshop on Learning word meaning from non-linguistic data - Volume 6": 24, # HLT-NAACL
#     "Proceedings of the fourth ACM conference on Digital libraries": 20, # JCDL
#     "HLT-NAACL-GEOREF '03 Proceedings of the HLT-NAACL 2003 workshop on Analysis of geographic references - Volume 1": 24, # HLT-NAACL
#     "ACL/IJCNLP (Student Research Workshop)": 7, # ACL
#     "Proceedings of the sixth ACM SIGKDD international conference on Knowledge discovery and data mining": 13, # KDD
#     "KDD Workshop on Data Mining and Audience Intelligence for Advertising": 13, # KDD
#     "NAACL (Demos)": 24, # HLT-NAACL
#     "Web Search and Data Mining": 54, # WSDM
#     "ACL Workshop on Natural Language Processing in the Biomedical Domain": 7, # ACL
#     "EACL (Student Research Workshop)": 34, # EACL
#     "Proceedings of the 1st international CIKM workshop on Topic-sentiment analysis for mass opinion": 5, # CIKM
#     "HLT-NAACL-TEXTMEANING '03 Proceedings of the HLT-NAACL 2003 workshop on Text meaning - Volume 9": 24, # HLT-NAACL
#     "SIGMOD '88 Proceedings of the 1988 ACM SIGMOD international conference on Management of data": 9, # SIGMOD
#     "HLT-NAACL--Demonstrations '04 Demonstration Papers at HLT-NAACL 2004": 24, # HLT-NAACL
#     "COLING '02 Proceedings of the 3rd workshop on Asian language resources and international standardization - Volume 12": 11 # COLING
# }




def read_and_parse():
    global index_count
    global tmp_counter
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

        if "references" in tmp_obj:
            for ref in tmp_obj["references"]:
                id_to_ref[index_count].append(ref)

        year_to_indexlist[year_string].append(index_count)
        index_count += 1
    conf_lines_file.close()



def generate_index_to_loc():
    tmp_file = open(largeVis_output)
    for line in tmp_file:
        vec = line.split()
        index_to_loc[vec[0]] = line
    # print(index_to_loc)
    tmp_file.close()


def generate_conf_index():
    global index_count
    for conf in conf_pool:
        conf_to_index[conf] = index_count
        print(conf)
        if conf in eq_name_map:
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
    for k, v in index_to_conf.items():
        out_edges_file.write(str(k) + " " + str(conf_to_index[v]) + " 2\n");
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
            if str(tmp) not in index_to_loc:
                continue
            layer_list[cur_layer].append(tmp)
        # print(k)
        if str(k) in split_points:
            cur_layer += 1
    # print(len(layer_list))
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
    for conf in eq_name_map.keys():
        print(index_to_loc[eq_name_to_index[conf]])
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

    print(color_map)
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
    main()


