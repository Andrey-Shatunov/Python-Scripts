from itertools import groupby

with open("input.txt", "r") as f: 
    n = int(f.readline()) 
    a = [int(i) for i in f.readline().split()]

a.sort()

tmp = 0
tmp_length = 0

for k,i in groupby(a):
    ln = len(list(i))

    if ln > tmp_length:
        tmp_length = ln
        tmp = k
    elif ln == tmp_length and k > tmp:
        tmp_length =ln
        tmp = k

print(tmp)