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
if args.label != '':
    for line in open(args.label):
        label.append(line.strip())

for i in range(22):
    label.append(i)


N = M = 0
all_data = {}

for i in range(22):
    all_data.setdefault(str(i), []).append((100, 100))

for i, line in enumerate(open(args.input)):
    vec = line.strip().split(' ')
    if i == 0:
        N = int(vec[0])
        M = int(2)
    elif i <= N:
        if args.label == '':
            label.append(0)
        all_data.setdefault(label[i-1], []).append((float(vec[-2]), float(vec[-1])))

colors = plt.cm.rainbow(numpy.linspace(0, 1, len(all_data)))

print(colors)


#print(all_data)
print(len(colors))
for color, ll in zip(colors, sorted(all_data.keys())):
    x = [t[0] for t in all_data[ll]]
    y = [t[1] for t in all_data[ll]]

    if ll == "2":
        plt.plot(x, y, 'x', color = "#000000", markersize = 0.5)
    else:
        plt.plot(x, y, 'x', color = color, markersize = 0.1)
    # color[1] = 0.5
    # color[2] = 0.5
    # color[3] = 0.5
    # plt.plot(x, y, '.', color = color, markersize = 0.1)
if args.range != '':
    l = abs(float(args.range))
    plt.xlim(-l, l)
    plt.ylim(-l, l)
plt.xlim(-40, 40)
plt.ylim(-40, 40)
plt.savefig(args.output, dpi = 500)
