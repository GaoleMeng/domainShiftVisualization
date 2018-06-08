import numpy
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-input', default = '', help = 'input file')
parser.add_argument('-label', default = '', help = 'label file')
parser.add_argument('-output', default = '', help = 'output file')
parser.add_argument('-range', default = '', help = 'axis range')

args = parser.parse_args()

label = []
for i in range(53):
    label.append(str(i + 1))


# if args.label != '':
#     for line in open(args.label):
#         label.append(line.strip())

N = M = 0
all_data = {}
# for i, line in enumerate(open(args.input)):
#     vec = line.strip().split(' ')
#     if i == 0:
#         N = int(vec[0])
#         M = int(2)
#     elif i <= N:
#         if args.label == '':
#             label.append(0)
#         all_data.setdefault(label[i-1], []).append((float(vec[-2]), float(vec[-1])))



color_map = {
    "Commun. ACM": 1,
    "NIPS": 2,
    "CHI": 3,
    "SIGIR": 4,
    "CIKM": 5,
    "ICDE": 6,
    "ACL": 7,
    "ACM Multimedia": 8, #MM
    "SIGMOD Conference": 9,
    "JASIST": 10,
    "COLING": 11,
    "STOC": 12,
    "KDD": 13,
    "VLDB": 14,
    "JASIS": 15,
    "WWW": 16,
    "ICDM": 17,
    "TREC": 18,
    "CLEF (Working Notes)": 19, # CLEF
    "JCDL": 20,
    "UAI": 21,
    "CSCW": 22,
    "EMNLP": 23,
    "HLT-NAACL": 24,
    "IUI": 25,
    "SDM": 26,
    "DASFAA": 27,
    "EDBT": 28,
    "ECIR": 29,
    "COLT": 30,
    "SSDBM": 31,
    "AAAI/IAAI": 32, # AAAI
    "ICWSM": 33,
    "EACL": 34,
    "PODS": 35,
    "RecSys": 36,
    "CVPR (1)": 37, # CVPR
    "VLDB J.": 38, 
    "CVPR (2)": 37,
    "meeting of the association for computational linguistics": 7, # ACL
    "WSDM": 40,
    "CLEF": 19,
    "AIRS": 42,
    "SOSP": 43,
    "Journal of The American Society for Information Science and Technology": 10, # JASIST
    "uncertainty in artificial intelligence": 21, # UAI
    "International Conference on Machine Learning": 46, # ICML
    "World Wide Web Conference Series": 16, # WWW
    "Multimedia Information Retrieval": 48,
    "COLING (Posters)": 49, # COLING
    "International Joint Conference on Artificial Intelligence": 50, # IJCAI
    "HLT": 24, # HLT-NAACL
    "Neural Information Processing Systems": 2,
    "WWW Posters": 16, # WWW
    "EMNLP-CoNLL": 23, # EMNLP
    "ACL (Short Papers)": 7, # ACL
    "International Conference on Information and Knowledge Management": 5, # CIKM
    "Meeting of the Association for Computational Linguistics": 7, # ACL
    "COLING-ACL": 7, # ACL
    "Conference on Computer Supported Cooperative Work": 22, # CSCW
    "International Conference on Data Engineering": 6, # ICDE
    "WWW (Special interest tracks and posters)": 16, # WWW
    "Very Large Data Bases": 14, # VLDB
    "WWW (Alternate Track Papers & Posters)": 16, # WWW
    "IJCAI (1)": 50, # IJCAI
    "HLT/EMNLP": 23, # EMNLP
    "Text REtrieval Conference": 18, # TREC
    "international world wide web conferences": 16, # WWW
    "HLT-NAACL (Short Papers)": 24, # HLT-NAACL
    "Conference of the European Chapter of the Association for Computational Linguistics": 34, # EACL
    "ACL/IJCNLP": 7, # ACL
    "ACM/IEEE Joint Conference on Digital Libraries": 20, # JCDL
    "HLT '89 Proceedings of the workshop on Speech and Natural Language": 24, # HLT-NAACL
    "CLEF (Notebook Papers/LABs/Workshops)": 19, # CLEF
    "Research and Development in Information Retrieval": 4, # SIGIR
    "conference on information and knowledge management": 5, # CIKM
    "Digital Libraries": 20, # JCDL
    "HLT '91 Proceedings of the workshop on Speech and Natural Language": 24, # HLT-NAACL
    "Uncertainty in Artificial Intelligence": 21, # UAI
    "Knowledge Discovery and Data Mining": 13, # KDD
    "north american chapter of the association for computational linguistics": 24, # HLT-NAACL
    "ACL/IJCNLP (Short Papers)": 7, # ACL
    "NAACL": 24, # HLT-NAACL
    "Cross-Language Evaluation Forum": 19, # CLEF
    "Intelligent User Interfaces": 25, # 
    "North American Chapter of the Association for Computational Linguistics": 24, # HLT-NAACL
    "HLT '02 Proceedings of the second international conference on Human Language Technology Research": 24, # HLT-NAACL
    "conference on computer supported cooperative work": 22, # CSCW
    "HLT '93 Proceedings of the workshop on Human Language Technology": 24, # HLT-NAACL
    "International Conference on Computer Vision": 51, # ICCV
    "HLT '01 Proceedings of the first international conference on Human language technology research": 24, # HLT-NAACL
    "CHI '82 Proceedings of the 1982 Conference on Human Factors in Computing Systems": 3, # CHI
    "Journal of the American Society for Information Science": 15, # JASIS
    "IEEE International Conference on Data Mining": 17, # ICDM
    "CHI '83 Proceedings of the SIGCHI Conference on Human Factors in Computing Systems": 3, # CHI
    "knowledge discovery and data mining": 13, # KDD
    "ACM Multimedia": 8, # MM
    "ACM Multimedia (1)": 8, # MM
    "CHI '87 Proceedings of the SIGCHI/GI Conference on Human Factors in Computing Systems and Graphics Interface": 3, # CHI
    "Conference on Information and Knowledge Management": 5, # CIKM
    "CHI '86 Proceedings of the SIGCHI Conference on Human Factors in Computing Systems": 3, # CHI
    "International Conference on Database Theory": 52, # ICDT
    "CHI '88 Proceedings of the SIGCHI Conference on Human Factors in Computing Systems": 3, # CHI
    "CLEF (1)": 19, # CLEF
    "Digital Libraries'99": 20, # JCDL
    "HLT-NAACL-Short '04 Proceedings of HLT-NAACL 2004: Short Papers": 24, # HLT-NAACL
    "TREC Video Retrieval Evaluation": 18, # TREC
    "international acm sigir conference on research and development in information retrieval": 4, # SIGIR
    "EMNLP '02 Proceedings of the ACL-02 conference on Empirical methods in natural language processing - Volume 10": 23, # EMNLP
    "KDD Cup": 13, # KDD
    "Empirical Methods in Natural Language Processing": 23, # EMNLP
    "KDD Workshop": 13, "KDD"
    "CSLDAMT '10 Proceedings of the NAACL HLT 2010 Workshop on Creating Speech and Language Data with Amazon's Mechanical Turk": 24, # HLT-NAACL
    "SIGMOD '12 Proceedings of the 2012 ACM SIGMOD International Conference on Management of Data": 9, # SIGMOD
    "CLEF (2)": 19, # CLEF
    "ACLdemo '04 Proceedings of the ACL 2004 on Interactive poster and demonstration sessions": 7, # ACL
    "SIGMOD Workshop, Vol. 2": 9, # SIGMOD
    "empirical methods in natural language processing": 23, # EMNLP
    "CHI '85 Proceedings of the SIGCHI Conference on Human Factors in Computing Systems": 3, # CHI
    "EMNLP '03 Proceedings of the 2003 conference on Empirical methods in natural language processing": 23, # EMNLP
    "MULTIMEDIA '96 Proceedings of the fourth ACM international conference on Multimedia": 8, # MM
    "EMNLP '00 Proceedings of the 2000 Joint SIGDAT conference on Empirical methods in natural language processing and very large corpora: held in conjunction with the 38th Annual Meeting of the Association for Computational Linguistics - Volume 13": 23, # EMNLP
    "very large data bases": 14, # VLDB
    "Human Language Technology": 53, # HLT/NAACL
    "international conference on weblogs and social media": 33, # ICWSM
    "ACM Multimedia EMME Workshop": 8, # MM
    "KDD Workshop on Human Computation": 13, # KDD
    "european conference on information retrieval": 29, # ECIR
    "CIKM-iNEWS": 5, # CIKM
    "ICCV '98 Proceedings of the Sixth International Conference on Computer Vision": 51, # ICCV
    "COLING '69 Proceedings of the 1969 conference on Computational linguistics": 11, # COLING
    "Proceedings of the 22nd annual international ACM SIGIR conference on Research and development in information retrieval": 4, # SIGIR
    "SNA@ICML": 46, # ICML
    "HLT-NAACL-LWM '04 Proceedings of the HLT-NAACL 2003 workshop on Learning word meaning from non-linguistic data - Volume 6": 24, # HLT-NAACL
    "Proceedings of the fourth ACM conference on Digital libraries": 20, # JCDL
    "HLT-NAACL-GEOREF '03 Proceedings of the HLT-NAACL 2003 workshop on Analysis of geographic references - Volume 1": 24, # HLT-NAACL
    "ACL/IJCNLP (Student Research Workshop)": 7, # ACL
    "Proceedings of the sixth ACM SIGKDD international conference on Knowledge discovery and data mining": 13, # KDD
    "KDD Workshop on Data Mining and Audience Intelligence for Advertising": 13, # KDD
    "NAACL (Demos)": 24, # HLT-NAACL
    "Web Search and Data Mining": 54, # WSDM
    "ACL Workshop on Natural Language Processing in the Biomedical Domain": 7, # ACL
    "EACL (Student Research Workshop)": 34, # EACL
    "Proceedings of the 1st international CIKM workshop on Topic-sentiment analysis for mass opinion": 5, # CIKM
    "HLT-NAACL-TEXTMEANING '03 Proceedings of the HLT-NAACL 2003 workshop on Text meaning - Volume 9": 24, # HLT-NAACL
    "SIGMOD '88 Proceedings of the 1988 ACM SIGMOD international conference on Management of data": 9, # SIGMOD
    "HLT-NAACL--Demonstrations '04 Demonstration Papers at HLT-NAACL 2004": 24, # HLT-NAACL
    "COLING '02 Proceedings of the 3rd workshop on Asian language resources and international standardization - Volume 12": 11 # COLING
}


def find_corresponding(num):
    ans = ""
    for k, v in color_map.items():
        if ans == "" and v == int(num):
            ans = k
        elif v == int(num) and len(ans) > len(k):
            ans = k
    return ans


N = int(53)
M = int(2)
for i in range(53):
    all_data.setdefault(label[i], []).append((float(0), float(23-i)))

print(sorted(all_data.keys()))
colors = plt.cm.rainbow(numpy.linspace(0, 1, len(all_data)))

for i in range(53):
    print(find_corresponding(i+1))


#print(all_data)
# print(colors)
for color, ll in zip(colors, sorted(all_data.keys())):
    x = [t[0] for t in all_data[ll]]
    y = [t[1] for t in all_data[ll]]
    print(ll)
    plt.plot(x, y, '.', color = color, markersize = 5)
if args.range != '':
    l = abs(float(args.range))
    plt.xlim(-l, l)
    plt.ylim(-l, l)
plt.xlim(-40, 40)
plt.ylim(-40, 40)
plt.savefig(args.output, dpi = 500)
#plt.show()

