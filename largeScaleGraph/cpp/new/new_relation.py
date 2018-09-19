import numpy
import matplotlib.pyplot as plt
import argparse
import matplotlib.patches as patches
import copy
import csv


chair_color = plt.cm.rainbow(numpy.linspace(0, 1, 8))


x_list = 0
y_list = [8, 7, 6, 5, 4, 3, 2, 1]

for i in range(8):
    if i == 3:
        plt.plot(x_list, y_list[i], '-o' ,color="#703c43")
    # elif i == 4:
    #     plt.plot(x_list, y_list[i], '-o' ,color="#598587")
    else:
        plt.plot(x_list, y_list[i], '-o' ,color=chair_color[i])

plt.ylim(-1, 10)
plt.show()


