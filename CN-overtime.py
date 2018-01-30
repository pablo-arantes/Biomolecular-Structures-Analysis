#The whole idea with the CN calculation is to evaluate the first solvation layer. For this, we must compute the optimum binding distance for this layer (which distance contemplates the first gaussian distribution). Thus, we should know beforehand this value to use as cutoff within the script. We just ran a single RDF calculation for 1 residue and look in which line the gaussian distribution ends (start counting after all headers). In theory, this distance should not change during the simulation.
#After that, you just insert the referred line into the 'cutoff' parameter within the script and it should find the optimal binding distance for you.

#USAGE: python CN-overtime 507

import os
import sys

ver = sys.argv[1]

simulation_time = '200000' 		#ps
output = 'CN-overtime.xvg'		# output name for CN-overtime.
g_rdfout = 'lala' 				# file will be named 'lala-number_of_frame-rdf.xvg' and 'lala-number_of_frame-rdf.xvg'
rdf_ref = 'Ala'					# reference to RDF calculation. Code must be the same as in .ndx file
rdf_target = 'Water'			# target to RDF calculation. Code must be the same as in .ndx file
tprfile = 'PIK.sim.tpr'			# Functional .tpr file from the trajectory
trajfile = 'PIK.sim.xtc'		# Functional .xtc or .trr file from the trajectory
ndxfile = 'index.ndx'			# Functional .ndx file with atoms/residues/molecules/ in individual entries to run RDF



cutoff = 250 					# number of lines (after Headers) to count on RDF search for maximum values. You should know this beforehand!!!!
step = 500						# ps. Will calculate CN within this amount of step time.

def run_rdf(ver):

	st = int(simulation_time)

	os.system("mkdir RDFs")
	for t in range(0,st,step):
		os.system("echo " + rdf_ref+ " " + rdf_target+ " | g_rdf_" + ver + " -s " + tprfile + " -f " + trajfile + " -n " + index.ndx + " -b " + str(t) + " -e " + str(t+step) + " -o RDFs/"+g_rdfout+"-"+str(t+step)+"-rdf.xvg -cn RDFs/"+g_rdfout+"-"+str(t+step)+"-cn.xvg")

def counter(file, HEAD1, HEAD2):
	point = 0
	head = 0
	
	arq = open(file, 'r')
	lines = arq.readlines()
	arq.seek(0)
	if len(lines) > 0:
		for i in range(len(lines)):
			line = arq.readline()
			if line.startswith(HEAD1) or line.startswith(HEAD2):
				head += 1
			else:
				if len(line) > 2:
					point += 1
	
	return head, point

def read_CN(file1, file2):
	###################################
	# Reading RDF file
	f1 = open(file1,"r")
	string = "text"

	headers1 = counter(file1, "@", "#")[0]
	radius_dic = {}

	for k in range(headers1):
		line = f1.readline()

	for k in range(cutoff):
		line = f1.readline()
		radius = line.split()[0]
		rdf = line.split()[1]
		radius_dic[rdf] = radius

	peak = max(radius_dic.keys())
	distance = radius_dic[max(radius_dic.keys())]

	###################################
	# Reading CN file
	f2 = open(file2,"r")
	string = "text"

	headers2 = counter(file2, "@", "#")[0]
	points2 = counter(file2, "@", "#")[1]

	for k in range(headers2):
		line = f2.readline()

	for k in range(points2):
		line = f2.readline()
		radius = line.split()[0]
		CN = line.split()[1]
		
		if radius == distance:
			break
	
	return CN, radius

def main(output):
	
	os.chdir("./RDFs/")
	
	st = int(simulation_time)
	out = open(output, 'w')
	out.write("""# This file was created by Glados!\n@    title "CN over time"\n@    xaxis  label "Time (ns)"\n@    yaxis  label "Coordination Number"\n@TYPE xy\n""")   
	t = 0 #ns initial time
	
	dt = st/step
	
	for z in range(0,st,step):
		CN = read_CN(g_rdfout+"-"+str(z+step)+"-rdf.xvg", g_rdfout+"-"+str(z+step)+"-cn.xvg")[0]
		
		time = str(t).ljust(10," ")
				
		out.write(time)
		out.write(CN)
		out.write('\n')
		
		t += dt
	out.close()


run_rdf(ver)
main(output)
