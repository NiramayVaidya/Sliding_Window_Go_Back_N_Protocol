from matplotlib import pyplot as plt
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', type=str, required=True, \
        help='give file name ahead of this flag')
args = parser.parse_args()
filename = args.file

f = open(filename, 'r')
x_axis_points = []
y_axis_points = []
line = f.readline()
while line:
    line = line.split(',')
    y_axis_points.append(float(line[0]))
    x_axis_points.append(float(line[1].strip()))
    line = f.readline()
f.close()

if filename.find('window') != -1:
    plt.xlabel('window size')
    plt.title('time vs window size graph for half duplex Go-Back-N protocol')
elif filename.find('frame') != -1:
    plt.xlabel('frame size')
    plt.title('time vs frame size graph for half duplex Go-Back-N protocol')
elif filename.find('probability') != -1:
    plt.xlabel('probability of dropping')
    plt.title('time vs probability of dropping graph for half duplex Go-Back-N protocol')
plt.ylabel('time in seconds')
plt.plot(x_axis_points, y_axis_points, linestyle='-', marker='o', color='r')
plt.show()
