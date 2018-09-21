import csv
import sys
import os
import matplotlib.pyplot as plt
import numpy

year_index_list = {}

conf_counter = 0

min_value = 1000000
with open('./conf_info.csv') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        conf_counter += 1
        min_value = min(min_value, int(row["label"]))

label_to_conf = {}
alias_to_conf = {}

with open('../csranking_list.txt') as f:
    for line in f:
        vec = line.strip().split("\t")
        print(vec)
        alias_to_conf[vec[1]] = vec[0]

def de_normalize(vec):
    ans = "#"
    for i in range(len(vec)-1):
        if int(vec[i] * 255) < 16:
            ans += "0"
        ans += str(hex(int(vec[i] * 255)))[2:]
    print(ans)
    return ans

with open('./conf_info.csv') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        label_to_conf[str(int(row["label"]) - min_value)] = alias_to_conf[row["conf_name"]]

    colors = plt.cm.rainbow(numpy.linspace(0, 1, len(alias_to_conf)))

    colors_str = []
    for i in range(len(colors)):
        colors_str.append(de_normalize(colors[i]))

    colors = colors_str

    key_to_color = {}
    for color, ll in zip(colors, sorted(label_to_conf.keys())):
        key_to_color[ll] = color

    for start in range(len(key_to_color)):
        plt.plot(0, start, '.', color = key_to_color[str(start)], markersize = 10)
        plt.text(1, start, label_to_conf[str(start)])
    plt.xlim(-2, 3)
    plt.ylim(-1, len(key_to_color) + 1)

    plt.show()


with open('./title_2dim_with_index_year_venue.csv') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        label = int(row["label"])
        year = int(row["year"])
        x = (row["x"])
        y = (row["y"])
        if year not in year_index_list:
            year_index_list[year] = []
        year_index_list[year].append((x, y, label))

new_list = sorted(year_index_list.iteritems())
file_index = 1
tmp = 0

for i in range(len(new_list)-4):
    output_file = open(str(i) + "_points.txt", "w")
    output_label = open(str(i) + "_labels.txt", "w")

    output_file.write(str(len(new_list[i][1]) + len(new_list[i+1][1]) + len(new_list[i+2][1]) + len(new_list[i+3][1]) + len(new_list[i+4][1])) + "\n")
    output_label.write(str(new_list[i][0]) + "~" + str(new_list[i][0] + 4) + "\n")
    for j in [i, i+1, i+2, i+3, i+4]:
        for tuu in new_list[j][1]:
            output_file.write("1 %s %s\n" % (tuu[0], tuu[1]))
            output_label.write(str(tuu[2]) + "\n")
    output_file.close()
    output_label.close()
    tmp = i

# output_file = open(str(50) + "_points.txt", "w")
# output_label = open(str(50) + "_labels.txt", "w")

# org_i = i
# total_length = 0
# for i in range(len(new_list)):
#     total_length += len(new_list[i][1])

# output_file.write(str(total_length) + "\n")
# for i in range(len(new_list)):
#     for tuu in new_list[i][1]:
#         output_file.write("1 %s %s\n" % (tuu[0], tuu[1]))
#         output_label.write(str(tuu[2]) + "\n")

# output_file.close()
# output_label.close()

# i = org_i
# i += 1
# output_file = open("49" + "_points.txt", "w")
# output_label = open("49" + "_labels.txt", "w")
# top_file_points = open("top5_points.txt").readlines()
# top_file_labels = open("top5_labels.txt").readlines()



# tmp_list = []
# label_list = []

# for j in [i-1, i, i+1, i+2, i+3]:
#     for tuu in new_list[j][1]:
#         tmp_list.append((tuu[0], tuu[1]))
#         label_list.append(str(tuu[2]))
#         # output_file.write("1 %s %s\n" % (tuu[0], tuu[1]))
#         # output_label.write(str(tuu[2]) + "\n")


# print("before label_list %s" % len(label_list))

# flag = 1
# # print(top_file_labels)
# for i in range(len(top_file_labels)):
#     if str(top_file_labels[i]).strip() in ["23", "25", "27", "29"]:
#         label_list.append("2")
#         vec = (top_file_points[i+1]).strip().split()
#         tmp_list.append((vec[1], vec[2]))

# print("after label_list %s" % len(label_list))

# output_file.write(str(len(tmp_list)) + "\n")
# assert(len(tmp_list) == len(label_list))
# for point in tmp_list:
#     output_file.write("1 %s %s\n" % (point[0], point[1]))

# for label in label_list:
#     output_label.write("%s\n" % label)

# output_file.close()
# output_label.close()

