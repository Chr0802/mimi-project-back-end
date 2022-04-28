import sys
import math

n = int(sys.stdin.readline())
attr = sys.stdin.readline().strip()
result = 0
for i in range(len(attr)):
    if attr[i] == "1":
        result += i
for i in range(1, len(attr)):
    w = v = 0
    for j in range(i):
        if attr[j] == "0":
            w += j + 1
    for k in range(i, len(attr)):
        if attr[k] == "1":
            v += k + 1
    if abs(w - v) < result:
        result = abs(w - v)
print(result)
