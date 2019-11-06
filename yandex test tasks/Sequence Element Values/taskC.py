from itertools import groupby

with open("input.txt", "r") as f: 
    n = int(f.readline()) 
    a = [int(i) for i in f.readline().split()]

mx = max(a)

lst = [0,1,2]

for i in range(3,max(a)+1):
    lst.append(lst[i-1] + lst[i-3])

print(" ".join(str(lst[i]) for i in a))