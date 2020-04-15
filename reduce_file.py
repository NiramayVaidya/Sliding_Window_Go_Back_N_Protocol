f1 = open('20k.txt', 'r')
f2 = open('1k.txt', 'w')

for i in range(0, 1000):
    f2.write(f1.readline())

f1.close()
f2.close()
