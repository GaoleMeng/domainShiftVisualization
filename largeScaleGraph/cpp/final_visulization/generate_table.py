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
    label.append(str(i))


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



color_map = {'ICML': 5, 'EMNLP': 17, 'CIKM': 3, 'SIGMOD': 7, 'JCDL': 14, 'UAI': 15, 'JASIST': 8, 'ACL': 4, 'SIGIR': 2, 'MM': 6, 'TREC': 12, 'CLEF': 13, 'KDD': 9, 'CHI': 1, 'WSDM': 21, 'VLDB': 10, 'CSCW': 16, 'RecSys': 20, 'NIPS': 0, 'WWW': 11, 'ECIR': 18, 'ICWSM': 19}

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
print(sorted(all_data.keys()))
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

