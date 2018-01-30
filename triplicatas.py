#Produces averages and standard deviations of identical data sets from, e.g. replicate simulations.

import sys
import numpy
import math

prefix = sys.argv[1]
 
def count_lines(file):              # function to count lines
    arq_in = open(file,"r")
    lines = -1
    while 1:                            
        line = arq_in.readline()
        lines = lines + 1
        if not line: break
    return lines
 
def sweep(dic_of_files):           
	file_1 = open(dic_of_files[1],"r")   ## Opening files
	file_2 = open(dic_of_files[2],"r")   
	file_3 = open(dic_of_files[3],"r")    
	 
	num_lines_1 = count_lines(str(dic_of_files[1]))     # counting number of lines in files
	num_lines_2 = count_lines(str(dic_of_files[2]))
	num_lines_3 = count_lines(str(dic_of_files[3]))
	 
	############################# consistencia linhas de arquivos diferentes  #######################################  
	if num_lines_1 != num_lines_2 or num_lines_2 != num_lines_3 or num_lines_1 != num_lines_3:
		print ">>> Number of lines is not the same!"
		print ">>> Please, check your input!"
		sys.exit(0)
	##################################################################################################################     
	else:
		print ">>> Number of lines is the same!"
				  

	 
	line1 = "#"
	k = 0
	time_1 = 0
	time_0 = 0
	 
	 
	for i in range(1):                                # Calculates dt
		while line1[0] == "#" or line1[0] == "@":     # Count number of header lines
			line1 = file_1.readline()
			k = k + 1

		 
		line1 = file_1.readline()

		time_1 = float(line1.split()[0])
		 
		line1 = file_1.readline()
		time_2 = float(line1.split()[0])
		 
		dt = time_2 - time_1 
		 
		 
		print ">>> dt =:",dt,"picoseconds."
		print ">>> Calculating..."
		 
		file_1.seek(0)                              # reset file reading
		 
		for i in range(k-1):                          # jump readers
			line1 = file_1.readline()
			line2 = file_2.readline()
			line3 = file_3.readline()
			line4 = file_4.readline()
			line5 = file_5.readline()
	 
	output = prefix+".rms-av.xvg"
	 
	 
	arq_out = open(output,"w")
	arq_out.close()
	arq_out = open(output,"a+")
	arq_out.write("""# This file was created by Glados!\n@    title "RMSD"\n@    xaxis  label "Time (ns)"\n@    yaxis  label "RMSD (nm)"\n@TYPE xy\n@ subtitle "RNA after lsq fit to RNA"\n""")     
	 
	for i in range(0,num_lines_1-k+1):             # Goes through files collecting terms

		raw_list = []

		line1 = file_1.readline()
		line2 = file_2.readline()
		line3 = file_3.readline()

	 
		time = float(line1.split()[0])    # collecting time
		 
		term1 = float(line1.split()[1])   # colecting term from file1
		term2 = float(line2.split()[1])
		term3 = float(line3.split()[1])

		 
		raw_list.append(term1)
		raw_list.append(term2)
		raw_list.append(term3)
	 
		standard = numpy.std(raw_list)      # standard deviation calculation
			 
		terms_sum = float(term1**2) + float(term2**2) + float(term3**2)    # Sum
		average = (terms_sum/3)**(0.5)                                        # taking averages
		 
		average = str(round(average, 5))                                # rounding to 5 numbers
		stdev = str(round(standard, 5))                                 # same
		time = float(time)/1000                      # converting to ns
		time = str(time)
	  
		
		average = average.ljust(10," ")
		sd = stdev.ljust(1," ")
		time = time.ljust(8," ")
		
		
			
		arq_out.write(str(time))
		arq_out.write(str(average))
		arq_out.write(str(sd))
		arq_out.write("\n")
        
         
def main(prefix):
	dic_of_files = {}
	
	print ">>> Hi! I was designed to run averages from 3 values. Let's begin!\n"
	
	dic_of_files[1] = str(prefix+".rms.1.xvg")
	dic_of_files[2] = str(prefix+".rms.2.xvg")
	dic_of_files[3] = str(prefix+".rms.3.xvg")
	
	sweep(dic_of_files)
	print ">>>Done!\n"
 
main(prefix)
