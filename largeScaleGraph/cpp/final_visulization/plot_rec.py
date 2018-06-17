import numpy
import matplotlib.pyplot as plt
import argparse
import matplotlib.patches as patches

parser = argparse.ArgumentParser()

parser.add_argument('-input', default = '', help = 'input file')
parser.add_argument('-label', default = '', help = 'label file')
parser.add_argument('-output', default = '', help = 'output file')
parser.add_argument('-range', default = '', help = 'axis range')

args = parser.parse_args()
density = 0.25



label = []
if args.label != '':
    for line in open(args.label):
        label.append(line.strip())

for i in range(22):
    label.append(i)


N = M = 0
all_data = {}


# map from integer locations to label count
rec_data = {}


def de_normalize(vec):
    ans = "#"
    
    for i in range(len(vec)-1):
        if int(vec[i] * 255) < 16:
            ans += "0"
        ans += str(hex(int(vec[i] * 255)))[2:]
    print(ans)
    return ans


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

        right_upper_x = 0
        right_upper_y = 0

        if float(vec[-2]) < 0:
            right_upper_x = int(float(vec[-2]) / density)
        else:
            right_upper_x = int(float(vec[-2]) / density) + 1
        
        if float(vec[-1]) < 0:
            right_upper_y = int(float(vec[-1]) / density)
        else:
            right_upper_y = int(float(vec[-1]) / density) + 1

        loc_str = str(right_upper_x) + " " + str(right_upper_y)
        if loc_str not in rec_data:
            rec_data[loc_str] = {}
        if label[i-1] not in rec_data[loc_str]:
            rec_data[loc_str][label[i-1]] = 0
        rec_data[loc_str][label[i-1]] += 1
        
        

colors = plt.cm.rainbow(numpy.linspace(0, 1, len(all_data)))

colors_str = []
for i in range(len(colors)):
    colors_str.append(de_normalize(colors[i]))


colors = colors_str

#print(all_data)
print(len(colors))
print(sorted(all_data.keys()))

tmp_counter = 0

key_to_color = {}
for color, ll in zip(colors, sorted(all_data.keys())):
    key_to_color[ll] = color


for location_str, counter_dict in rec_data.items():
    ru_x = int(location_str.split()[0])
    ru_y = int(location_str.split()[1])

    location_x_list = [ru_x * density, (ru_x - 1) * density, (ru_x - 1) * density, ru_x * density]
    location_y_list = [ru_y * density, ru_y * density, (ru_y - 1) * density, (ru_y - 1) * density]

    most_label = ""
    most_count = 0
    for k, v in counter_dict.items():
        if v > most_count:
            most_label = k
            most_count = v

    if most_count > 1:
        if most_label == "2":
            plt.fill(location_x_list, location_y_list, color=key_to_color[most_label], edgecolor="#000000")
        else:
            plt.fill(location_x_list, location_y_list, color=key_to_color[most_label], edgecolor="none")






# for color, ll in zip(colors, sorted(all_data.keys())):
#     x = [t[0] for t in all_data[ll]]
#     y = [t[1] for t in all_data[ll]]

#     if ll == "12":
#         plt.plot(x, y, '.', color = "#000000", markersize = 0.5)
#         tmp_counter += len(all_data[ll])
#     # # elif ll == "10":
#     # #     plt.plot(x, y, 'x', color = "#000000", markersize = 0.1)
#     # else:
#     plt.plot(x, y, 'x', color = color, markersize = 0.1)
#     # color[1] = 0.5
#     # color[2] = 0.5
#     # color[3] = 0.5
#     # plt.plot(x, y, '.', color = color, markersize = 0.1)

print("sigir this time:", tmp_counter)
if args.range != '':
    l = abs(float(args.range))
    plt.xlim(-l, l)
    plt.ylim(-l, l)
plt.xlim(-40, 40)
plt.ylim(-40, 40)
plt.savefig(args.output, dpi = 500)
