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
for i in range(22):
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



color_map = {'KDD Cup': 9, 'Proceedings of the 1st international CIKM workshop on Topic-sentiment analysis for mass opinion': 3, 'CLEF': 13, 'WWW (Alternate Track Papers & Posters)': 11, 'ACL/IJCNLP (Short Papers)': 4, 'EMNLP': 17, 'ACL (Short Papers)': 4, 'Journal of The American Society for Information Science and Technology': 8, 'UAI': 15, 'conference on computer supported cooperative work': 16, 'ACM Multimedia EMME Workshop': 6, 'CHI': 1, 'Meeting of the Association for Computational Linguistics': 4, "EMNLP '03 Proceedings of the 2003 conference on Empirical methods in natural language processing": 17, 'WSDM': 21, 'KDD Workshop': 9, "EMNLP '00 Proceedings of the 2000 Joint SIGDAT conference on Empirical methods in natural language processing and very large corpora: held in conjunction with the 38th Annual Meeting of the Association for Computational Linguistics - Volume 13": 17, 'International Conference on Machine Learning': 5, 'TREC': 12, 'JCDL': 14, 'Web Search and Data Mining': 21, 'very large data bases': 10, 'CLEF (Working Notes)': 13, 'WWW Posters': 11, 'ACM Multimedia (2)': 6, 'Proceedings of the sixth ACM SIGKDD international conference on Knowledge discovery and data mining': 9, 'EMNLP-CoNLL': 17, 'ECIR': 18, 'Text REtrieval Conference': 12, 'Neural Information Processing Systems': 0, 'KDD Workshop on Human Computation': 9, 'CLEF (Notebook Papers/LABs/Workshops)': 13, 'International Conference on Information and Knowledge Management': 3, 'uncertainty in artificial intelligence': 15, 'Very Large Data Bases': 10, 'conference on information and knowledge management': 3, 'JASIST': 8, 'ICML': 5, 'Proceedings of the 22nd annual international ACM SIGIR conference on Research and development in information retrieval': 2, 'VLDB J.': 10, 'Digital Libraries': 14, "MULTIMEDIA '96 Proceedings of the fourth ACM international conference on Multimedia": 6, "CHI '88 Proceedings of the SIGCHI Conference on Human Factors in Computing Systems": 1, 'Conference on Computer Supported Cooperative Work': 16, 'ICWSM': 19, "CHI '83 Proceedings of the SIGCHI Conference on Human Factors in Computing Systems": 1, 'SNA@ICML': 5, 'ACL Workshop on Natural Language Processing in the Biomedical Domain': 4, 'KDD': 9, 'knowledge discovery and data mining': 9, 'Journal of the American Society for Information Science': 8, "SIGMOD '12 Proceedings of the 2012 ACM SIGMOD International Conference on Management of Data": 7, 'meeting of the association for computational linguistics': 4, 'international acm sigir conference on research and development in information retrieval': 2, 'ACL': 4, 'european conference on information retrieval': 18, "CHI '85 Proceedings of the SIGCHI Conference on Human Factors in Computing Systems": 1, 'SIGMOD Workshop, Vol. 2': 7, 'CIKM': 3, "CHI '87 Proceedings of the SIGCHI/GI Conference on Human Factors in Computing Systems and Graphics Interface": 1, 'RecSys': 20, 'SIGMOD Conference': 7, 'WWW': 11, 'Uncertainty in Artificial Intelligence': 15, 'KDD Workshop on Data Mining and Audience Intelligence for Advertising': 9, 'CLEF (1)': 13, 'Cross-Language Evaluation Forum': 13, 'TREC Video Retrieval Evaluation': 12, "ACLdemo '04 Proceedings of the ACL 2004 on Interactive poster and demonstration sessions": 4, "CHI '86 Proceedings of the SIGCHI Conference on Human Factors in Computing Systems": 1, 'JASIS': 8, "SIGMOD '88 Proceedings of the 1988 ACM SIGMOD international conference on Management of data": 7, 'ACL/IJCNLP': 4, 'Empirical Methods in Natural Language Processing': 17, 'international world wide web conferences': 11, 'ACL/IJCNLP (Student Research Workshop)': 4, 'international conference on weblogs and social media': 19, 'CLEF (2)': 13, 'CIKM-iNEWS': 3, 'Knowledge Discovery and Data Mining': 9, 'ACM Multimedia 2001': 6, 'COLING-ACL': 4, 'SIGIR': 2, 'ACM Multimedia (1)': 6, 'Conference on Information and Knowledge Management': 3, 'Proceedings of the fourth ACM conference on Digital libraries': 14, 'ACM/IEEE Joint Conference on Digital Libraries': 14, 'VLDB': 10, "CHI '82 Proceedings of the 1982 Conference on Human Factors in Computing Systems": 1, "EMNLP '02 Proceedings of the ACL-02 conference on Empirical methods in natural language processing - Volume 10": 17, "Digital Libraries'99": 14, 'WWW (Special interest tracks and posters)': 11, 'Research and Development in Information Retrieval': 2, 'CSCW': 16, 'World Wide Web Conference Series': 11, 'empirical methods in natural language processing': 17, 'NIPS': 0}


def find_corresponding(num):
    ans = ""
    for k, v in color_map.items():
        if ans == "" and v == int(num):
            ans = k
        elif v == int(num) and len(ans) > len(k):
            ans = k
    return ans


N = int(22)
M = int(2)
for i in range(22):
    all_data.setdefault(label[i], []).append((float(0), float(23-i)))

print(sorted(all_data.keys()))
colors = plt.cm.rainbow(numpy.linspace(0, 1, len(all_data)))


print(len(colors))
for i in range(22):
    print(find_corresponding(i))


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

