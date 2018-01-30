import os
import sys

# This script calculate the difference between 2 RMSF files.

# Usage: python rmsf_diferencial.py file1 file2 , where the difference will be calculated as: DIF = value1 - value 2. Use your files with wisdom.



file1 = sys.argv[1]
file2 = sys.argv[2]

def count_lines(file):              # function to count lines
    arq_in = open(file,"r")
    lines = -1
    while 1:                            
        line = arq_in.readline()
        lines = lines + 1
        if not line: break
    return lines
    
    
def sweep(dic_of_files, output):           
	file_1 = open(dic_of_files[1],"r")   ## Opening files
	file_2 = open(dic_of_files[2],"r")
	
	num_lines_1 = count_lines(str(dic_of_files[1]))     # counting number of lines in files
	num_lines_2 = count_lines(str(dic_of_files[2]))
	
	if num_lines_1 != num_lines_2:
		print ">>> Number of lines is not the same!"
		print ">>> Please, check your input!"
		sys.exit(0)
	else:
		print ">>> Number of lines is the same!"

	##########################################################################################
	 
	 
	arq_out = open(output,"w")
	arq_out.close()
	arq_out = open(output,"a+")
	arq_out.write("""# This file was created by Glados!\n@    title "Diferential RMSF"\n@    xaxis  label "Residue"\n@    yaxis  label "RMSF (nm)"\n@TYPE xy\n""")     

	##########################################################################################
	
	line1 = "#"
	k = 0	 
	 
	for i in range(1):
		while line1[0] == "#" or line1[0] == "@":     # Count number of header lines
			line1 = file_1.readline()
			k = k + 1
		 
		file_1.seek(0)                              # reset file reading
		 
		for i in range(k-1):                          # jump readers
			line1 = file_1.readline()
			line2 = file_2.readline()
	
	
	for i in range(0,num_lines_1-k+1):             # Goes through files collecting terms

		raw_list = []

		line1 = file_1.readline()
		line2 = file_2.readline()
		
		res = float(line1.split()[0])    # collecting residue
		 
		term1 = float(line1.split()[1])   # colecting term from file1
		term2 = float(line2.split()[1])
		
		dif = float(term1) - float(term2)    # Sum
		 
		dif = str(round(dif, 5))                                # rounding to 5 numbers
		res = str(res)
	  
		
		dif = dif.ljust(10," ")
		res = res.ljust(8," ")
		
		
			
		arq_out.write(str(res))
		arq_out.write(str(dif))
		arq_out.write("\n")
		
def main(file1, file2):
	dic_of_files = {}
	
	print ">>> Hi! I was designed to run difference between 2 RMSF. Let's begin!\n"
	
	dic_of_files[1] = str(file1)
	dic_of_files[2] = str(file2)
	
	output = "Dif-rmsf.xvg"
	
	sweep(dic_of_files, output)
	print ">>>Done!\n"
 
main(file1, file2)	
