import argparse
import sys
import random
import socket
import time

parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', type=str, required=True, \
        help='give file name ahead of this flag')
parser.add_argument('--minrtt', '-mnrtt', type=int, required=True, \
        help='give min rtt value ahead of this flag')
parser.add_argument('--maxrtt', '-mxrtt', type=int, required=True, \
        help='give max rtt value ahead of this flag')
args = parser.parse_args()
filename = args.file
minrtt = args.minrtt
maxrtt = args.maxrtt

f = open(filename, 'w')

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

receiver_port = 8082

s.bind(('', receiver_port))
print('Receiver ready on socket localhost:8082')

seqnum = -1
datanums = []
typeofframe = 1

time_start = time.time()

while True:
    try:
        data, addr = s.recvfrom(1505)
    except socket.timeout:
        break
    while data:
        data = data.decode().split(' ')
        if int(data[0]) == (seqnum + 1):
            seqnum = seqnum + 1
            datanums.append(int(data[0]))
            f.write(data[2])
        elif int(data[0]) == 0:
            seqnum = 0
            datanums.append(int(data[0]))
            f.write(data[2])
        print('Frame ' + str(data[0]) + ' received')
        s.settimeout(2)
        try:
            data, addr = s.recvfrom(1505)
        except socket.timeout:
            data = None
    print('\n')
    for i in range(0, len(datanums)):
        u = random.uniform(0, 1)
        countdown = minrtt + (maxrtt - minrtt) * u
        time.sleep(countdown)
        send_data = str(datanums[i]) + ' ' + str(typeofframe)
        s.sendto(send_data.encode(), addr)
    datanums.clear()
    s.settimeout(50)

time_end = time.time()
f.close()
s.close()
print('Receiver socket closed')
print('File succesfully received')
print('Time required- ' + str(time_end - time_start))

