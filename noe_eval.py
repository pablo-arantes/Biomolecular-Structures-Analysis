import os
import sys
import numpy

##########################################
# Usage: python noe.py arquivo_de_angulos.xvg'
# o arquivo de distancias está definido na linha 11
##########################################

prefix = sys.argv[1]
dist_arq = 'dist.xvg'

cutoff = 0.3 # in nm

def count_lines(file):              # function to count lines
    arq_in = open(file,"r")
    lines = -1
    while 1:                            
        line = arq_in.readline()
        lines = lines + 1
        if not line: break
    
    arq_in.seek(0) 
    
    line1 = "#"
    k = 0
    
    for i in range(1):
		while line1[0] == "#" or line1[0] == "@":     # Count number of header lines
			line1 = arq_in.readline()
			k = k + 1
    
    headers = k
    
    return lines, headers

def sweep_dist(prefix):
	file = open(prefix,"r")   ## Opening files
	
	k = count_lines(prefix)[1]
	nl = count_lines(prefix)[0]

	for i in range(k-1):
		line = file.readline()
	
	time = []
	
	for i in range(nl):
		line = file.readline()
		if len(line.split()) > 0:
			dist = float(line.split()[1])
			if dist < cutoff:
				value0 = float(line.split()[0])
				time.append(value0)
	
	return time

def sweep(prefix):           
	
	file = open(prefix,"r")   ## Opening files
	
	k = count_lines(prefix)[1]
	nl = count_lines(prefix)[0]
	
	time = sweep_dist(dist_arq)
	
	frames = []
	angle = []
	
	for i in range(k-1):
		line = file.readline()
	
	for i in range(nl):
		line = file.readline()
		if len(line.split()) > 0:
			value0 = float(line.split()[0])
			value1 = float(line.split()[1])
			if value0 in time:
				frames.append(value0)
				angle.append(value1)
			else:
				pass
	
	for x in angle:
		print x
	
	standard = numpy.std(angle)
	average = numpy.average(angle)
	
	print "#####################################"
	print ">>> Grepping angles with conformations with distance below: " + str(cutoff) + " nm"
	print
	print ">>> Average angle = " + str(average) + " +- "+ str(standard)
	print
	

sweep(prefix)
