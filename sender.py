import argparse
import re
import sys
import random
import socket

parser = argparse.ArgumentParser()
parser.add_argument('--recipaddr', '-recip', type=str, required=True, \
        help='give receiver ip address ahead of this flag')
parser.add_argument('--file', '-f', type=str, required=True, \
        help='give file name ahead of this flag')
parser.add_argument('--framesize', '-frs', type=int, required=True, \
        help='give frame size ahead of this flag')
parser.add_argument('--minrtt', '-mnrtt', type=int, required=True, \
        help='give min rtt value ahead of this flag')
parser.add_argument('--n', '-N', type=int, required=True, \
        help='give window size value N ahead of this flag')
parser.add_argument('--p', '-P', type=float, required=True, \
        help='give probability of dropping frame p ahead of this flag')
args = parser.parse_args()
rec_ip_addr = args.recipaddr
filename = args.file
framesize = args.framesize
minrtt = args.minrtt
n = args.n
p = args.p

match = re.search(r'(\d+)\.(\d+)\.(\d+)\.(\d+)', rec_ip_addr)
if match:
    for i in range(1, 5):
        temp = int(match.group(i))
        if temp > 255 or temp < 0:
            print('Enter valid ip address -> something between 0.0.0.0 and \
                    255.255.255.255')
            sys.exit()
else:
    print('Enter valid ip address -> something between 0.0.0.0 and \
            255.255.255.255')
    sys.exit()

try:
    f = open(filename, 'r')
except FileNotFoundError:
    print('Enter valid filename -> file does not exist')
    sys.exit()

if p > 1 or p < 0:
    print('Enter valid probability -> something between 0 and 1 both inclusive')
    sys.exit()

if framesize > (1500 + 5):
    framesize = 1505
    print('framesize can be a maximum of 1505 -> floored to 1505')
elif framesize < (4 + 1):
    framesize = 5
    print('framesize cannot be less than 5 -> ceiled to 5')

all_frames = []
data = f.read(framesize - 5)
if n > 16:
    n = 16
    print('window size can be a max of 16 -> floored to 16')
elif n <= 0:
    n = 1
    print('window size cannot be less than 1 -> ceiled to 1')
seqnumlimit = n + 1
seqnum = 0
typeofframe = 0
while data:
    all_frames.append(str(seqnum) + ' ' + str(typeofframe) + ' ' + data)
    seqnum = (seqnum + 1) % seqnumlimit
    data = f.read(framesize - 5)

f.close()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sender_port = 8081
receiver_port = 8082

s.bind(('', sender_port))
print('Sender ready on socket localhost:8081')

win_start = 0
win_end = n
end = 0
if win_end > len(all_frames):
    win_end = len(all_frames)
    end = 1
countdown = minrtt * n
position = -1

while win_start < len(all_frames):
    for i in range(win_start, win_end):
        v = random.uniform(0, 1)
        if v > p:
            s.sendto(all_frames[i].encode(), (rec_ip_addr, receiver_port))
            print('Frame ' + (str(i % seqnumlimit)) + ' sent')
        else:
            print('Frame ' + (str(i % seqnumlimit)) + ' dropped')
    s.settimeout(float(countdown))
    print('Timer set')
    try:
        for i in range(win_start, win_end):
            data, addr = s.recvfrom(16)
            data = data.decode().split(' ')
            position = int(data[0])
            print('ACK ' + str(position % seqnumlimit) + ' received')
        data, addr = s.recvfrom(16)
    except socket.timeout:
        if position == int(all_frames[win_end - 1].split()[0]):
            print('ACKs successfully received for all frames sent')
            if end == 1:
                win_start = len(all_frames)
                continue
            win_start = win_end
            win_end = win_end + n
        else:
            print('Timer hit')
            print('ACKs not successfully received for all frames sent')
            for i in range(win_start, win_end):
                if position == int(all_frames[i].split()[0]):
                    win_start = position + 1
                    win_end = position + 1 + n
        if win_end > len(all_frames):
            win_end = len(all_frames)
            end = 1

s.close()
print('Sender socket closed')
print('File successfully sent')



