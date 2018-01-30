import os
import sys

# USAGE = python scatter.py EIXO_X.xvg EIXO_Y.xvg

file1 = sys.argv[1]
file2 = sys.argv[2]

output = "output.xvg"

read1 = open(file1, 'r')
read2 = open(file2, 'r')
out = open(output, 'w')

line1 = read1.readline()
line2 = read2.readline()


while line1[0] == '#' or line1[0] == '@':
	line1 = read1.readline()

while line2[0] == '#' or line2[0] == '@':
	line2 = read2.readline()


while True:
	line1 = read1.readline()
	line2 = read2.readline()

	if not line1 or not line2: break

	if len(line1.split()) > 0 and len(line2.split()) > 0:

		value1 = line1.split()[1]
		value2 = line2.split()[1]

		v1 = value1.ljust(10, ' ')
		v2 = value2.ljust(10, ' ')
		string = v1 + v2 + "\n"
		out.write(string)

out.close()
