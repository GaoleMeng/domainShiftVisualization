import numpy
import matplotlib.pyplot as plt
import argparse
import matplotlib.patches as patches
import copy
import csv

parser = argparse.ArgumentParser()

parser.add_argument('-input', default = '', help = 'input file')
parser.add_argument('-label', default = '', help = 'label file')
parser.add_argument('-output', default = '', help = 'output file')
parser.add_argument('-range', default = '', help = 'axis range')


def de_normalize(vec):
    ans = "#"
    
    for i in range(len(vec)-1):
        if int(vec[i] * 255) < 16:
            ans += "0"
        ans += str(hex(int(vec[i] * 255)))[2:]
    print(ans)
    return ans



for tmp_i in [47]:
    
    args_label = str(tmp_i) + "_labels.txt"
    args_input = str(tmp_i) + "_points.txt"
    args_output = str(tmp_i) + ".png"
    args_range = ''

    args = parser.parse_args()
    density = 0.1
    smooth_threshold = 3
    single_ton = 6


    label = []
    if args_label != '':
        for line in open(args_label):
            label.append(line.strip())

    for i in range(22):
        label.append(i)


    N = M = 0
    all_data = {}
    label_to_capital = {}

    # map from integer locations to label count
    rec_data = {}



    for i in range(22):
        all_data.setdefault(str(i), []).append((41, 41))



    keywords_point_list = []


    for i, line in enumerate(open(args_input)):
        vec = line.strip().split(' ')
        if i == 0:
            N = int(vec[0])
            M = int(2)
        elif i <= N:
            if args_label == '':
                label.append(0)

            if label[i-1] == "22":
                keywords_point_list.append((float(vec[-2]), float(vec[-1])))
                continue

            tmp_label = label[i-1]

            if tmp_label == "19":
                tmp_label = "10"
            elif tmp_label == "10":
                tmp_label = "19"
            elif tmp_label == "8":
                tmp_label = "2"
            elif tmp_label == "2":
                tmp_label = "8"
            elif tmp_label == "14":
                tmp_label = "20"
            elif tmp_label == "20":
                tmp_label = "14"
            elif tmp_label == "17":
                tmp_label = "21"
            elif tmp_label == "21":
                tmp_label = "17"
            elif tmp_label == "16":
                tmp_label = "9"
            elif tmp_label == "9":
                tmp_label = "16"
            
            if tmp_label == "21":
                tmp_label = "15"
            elif tmp_label == "15":
                tmp_label = "21"
            elif tmp_label == "17":
                tmp_label = "0"
            elif tmp_label == "0":
                tmp_label = "17"


            all_data.setdefault(tmp_label, []).append((float(vec[-2]), float(vec[-1])))

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
            if tmp_label not in rec_data[loc_str]:
                rec_data[loc_str][tmp_label] = 0
            rec_data[loc_str][tmp_label] += 1
            
            

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


    for k, point_list in all_data.items():
        sum_x = 0.0
        sum_y = 0.0
        for point in point_list:
            sum_x += point[0]
            sum_y += point[1]
        
        if len(point_list) == 1:
            print(sum_x, sum_y)
            continue
        
        label_to_capital[k] = ((sum_x-100) / (len(point_list)-1), (sum_y-100) / (len(point_list) - 1))
        if tmp_i == 100:
            # if int(k) == 8:
            #     plt.plot(label_to_capital[k][0], label_to_capital[k][1], 'o', color="#000000", markersize = 3.5, zorder=20, mec="#dd2323")
            # else:
            plt.plot(label_to_capital[k][0], label_to_capital[k][1], 'o', color=key_to_color[k], markersize = 3.5, zorder=20)
            


    for point in keywords_point_list:
        plt.plot(point[0], point[1], 'x', color = "#808080", markersize = 0.1, zorder=0)



    location_str_to_label = {}
    next_location_str_to_label = {}
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

        if most_count > 0:
            assert(most_label != "")
            location_str_to_label[location_str] = most_label
            # if most_label == "0":
            #     plt.fill(location_x_list, location_y_list, color=key_to_color[most_label], edgecolor="#000000")
            # else:
            #     plt.fill(location_x_list, location_y_list, color=key_to_color[most_label], edgecolor="none")

    dir_x = [1, 1, 1, 0, -1, -1, -1, 0]
    dir_y = [1, 0, -1, -1, -1, 0, 1, 1]

    for _ in range(5):
        next_location_str_to_label = copy.deepcopy(location_str_to_label)

        for x in range(int(40 / density) * 2):
            for y in range(int(40 / density) * 2):
                tmp_x = x - int(40 / density)
                tmp_y = y - int(40 / density)
                loc_str = str(tmp_x) + " " + str(tmp_y)

                label_counter = {}
                most_label = ""
                most_count = 0
                for i in range(8):
                    next_x = tmp_x + dir_x[i]
                    next_y = tmp_y + dir_y[i]
                    next_str = str(next_x) + " " + str(next_y)
                    if next_str not in location_str_to_label:
                        continue

                    if location_str_to_label[next_str] not in label_counter:
                        label_counter[location_str_to_label[next_str]] = 0
                    label_counter[location_str_to_label[next_str] ] += 1
                # print(label_counter)
                for k, v in label_counter.items():
                    if v > most_count:
                        most_label = k
                        most_count = v
                
                if most_count > smooth_threshold:
                    assert(most_label != "")
                    next_location_str_to_label[loc_str] = most_label

        location_str_to_label = next_location_str_to_label


    for _ in range(2):
        next_location_str_to_label = copy.deepcopy(location_str_to_label)
        for k, v in location_str_to_label.items():
            x = k.split()[0]
            y = k.split()[1]
            tmp_x = int(x)
            tmp_y = int(y)
            loc_str = str(tmp_x) + " " + str(tmp_y)

            label_counter = {}
            most_label = ""
            most_count = 0
            for i in range(8):
                next_x = tmp_x + dir_x[i]
                next_y = tmp_y + dir_y[i]
                next_str = str(next_x) + " " + str(next_y)
                # print(next_str)
                if next_str not in location_str_to_label:
                    most_count += 1
            
            if most_count > 7:
                # print("del")
                del(next_location_str_to_label[k])
        location_str_to_label = next_location_str_to_label

    # if tmp_i == 47:
    for location_str, most_label in location_str_to_label.items():
        ru_x = int(location_str.split()[0])
        ru_y = int(location_str.split()[1])

        location_x_list = [ru_x * density, (ru_x - 1) * density, (ru_x - 1) * density, ru_x * density]
        location_y_list = [ru_y * density, ru_y * density, (ru_y - 1) * density, (ru_y - 1) * density]

        # if most_label == "8":
        #     plt.fill(location_x_list, location_y_list, color="#000000", edgecolor="none", zorder=10)
        #     # plt.patches.Rectangle((location_x_list[1], location_y_list[2]), density, density)
        # else:
        # plt.fill(location_x_list, location_y_list, color=key_to_color[most_label], edgecolor="none", zorder=10)
        plt.fill(location_x_list, location_y_list, color="#d6d1d1", edgecolor="none", zorder=10)



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
    if args_range != '':
        l = abs(float(args_range))
        plt.xlim(-l, l)
        plt.ylim(-l, l)
    plt.xlim(-25, 25)
    plt.ylim(-25, 25)

    # if tmp_i == 48:
    #     plt.title("2012 ~ 2017")
    # elif tmp_i == 49:
    #     plt.title("2012 ~ 2018")
    # elif tmp_i == 50:
    #     plt.title("2012 ~ 2016")
    # elif tmp_i == 47:
    #     plt.title("2012 ~ 2018")
    # else:
    #     plt.title(str(2016 - 47 + tmp_i - 4) + " ~ " + str(2016 - 47 + tmp_i))
    
    # if tmp_i == 50:
        # plt.show()
    # plt.clf()




# point_file = open("./top-10-points.txt")
# label_file = open("./top-10-label.txt")

# point_list = point_file.readlines()
# label_list = label_file.readlines()

# for i in range(len(point_list)):
#     vec = point_list[i].strip().split()
#     if int(label_list[i].strip()) in [27, 28, 29, 30]:
#         plt.plot(float(vec[1]), float(vec[2]), 'x', color = "#2db5e5", markersize = 2, zorder=100)


# point_file.close()
# label_file.close()


with open('./SIGIR18_pc.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        
        plt.plot(float(row[1]), float(row[2]), 'x', color = "#1379c6", markersize = 2, zorder=90)


chair_color = plt.cm.rainbow(numpy.linspace(0, 1, 8))

with open('./SIGIR18_chairs_v2.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        if int(row[0]) - 1 == 3:
            plt.plot(float(row[2]), float(row[3]), '-o', color = "#703c43", markersize = 4, zorder=100)
        elif int(row[0]) - 1 == 0:
            plt.plot(float(row[2]), float(row[3]), '-o', color = chair_color[7], markersize = 4, zorder=100)
        elif int(row[0]) - 1 == 7:
            plt.plot(float(row[2]), float(row[3]), '-o', color = chair_color[0], markersize = 4, zorder=100)
        else:
            plt.plot(float(row[2]), float(row[3]), '-o', color = chair_color[int(row[0]) - 1], markersize = 4, zorder=100)





# with open('./SIGIR18_authors.csv', 'rb') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=',')
#     for row in spamreader:

#         plt.plot(float(row[1]), float(row[2]), 'x', color = "#db3636", markersize = 2, zorder=100)




plt.title("SIGIR 2018 PC and Chairs")

plt.savefig("2018_PC_chairs", dpi = 500)

