#!/usr/bin/env python2
#Thanks @yurichev for this post: https://yurichev.com/blog/cabling_Z3/

from z3 import If, Ints, Optimize, And, Distinct, Int
from string import ascii_uppercase as abc
from sys import argv


def check_count_device(a):
	l = []
	for i in a:
		if i.isupper(): l.append(i)
	return(len(list(set(l))))


def diff(x, y):
    return If(x<y, y-x, x-y)


def help():
	print("You have 3 network devices: A, B and C\nFrom A to B three cables, from A to C six cables and from B to C one cables. Your string: 'AB3 AC6 BC1'")
	print("Example run script:\npython2 cabling_z3.py 'AB3 AC6 BC1'")
	exit()


try:
	superstring = argv[1]
	if len(superstring) < 4:
		help()

except IndexError:
	help()

n = check_count_device(superstring)
d = {}
l = []
s=Optimize()

for i in range(n):
	d[abc[i]] = Int(abc[i])
	globals()[abc[i]] = Int(abc[i])
	l.append(abc[i])
	s.add(And(d[abc[i]]>=0, d[abc[i]]<=n-1))


s.add(Distinct([d[x] for x in l]))

for i in superstring.split(' '):
	s.add(Int('diff_{0}_{1}'.format(i[0],i[1]))==diff(d.get(i[0]), d.get(i[1])))
	try:
		final_sum += Int('diff_{0}_{1}'.format(i[0],i[1]))*int(i[2])
	except NameError:
		final_sum = Int('diff_{0}_{1}'.format(i[0],i[1]))*int(i[2])


final_sum2=Int("final_sum2")
s.add(final_sum==final_sum2)
s.minimize(final_sum)
s.check()
m=s.model()

a={}

for i in l:
	a[m[d[i]].as_long()]=str(i)

for i in range(n):
    print(a[i])

print('Minimum number of cables: {0}'.format(m[final_sum2]))
