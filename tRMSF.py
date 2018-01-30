# Usage: python tRMSF.py ver prefix dt
# Usage: python tRMSF.py 507 mon 1

import os
import sys

#############################
ver = sys.argv[1]
prefix = sys.argv[2]
dt = int(sys.argv[3])*1000 # janela de calculo de RMSF (em ns)
#############################

output = "tRMSF.xvg"
tpr = 'mon.tpr'
xtc = 'mon.xtc'
ndx = 'index.ndx'

############################
def calc(ver,prefix,dt):

    os.system("echo Protein-H Protein-H | g_rms_" + ver + " -s " + tpr + " -f " + xtc + " -n " + ndx + " -o " + prefix + ".rmsd.xvg")
    f = open(prefix + ".rmsd.xvg","r")
    string = "text"
    string = f.readlines()[-1]
    line = string.strip('\n')
    time_ps = int(round(float(line.split()[0])))

    if not os.path.exists('RMSF/'):
        os.system("mkdir RMSF")
    else:
        os.system("rm RMSF/*")

    for i in range(0,time_ps,dt):
        os.system("echo Protein-H | g_rmsf_" + ver + " -s " + tpr + " -f " + xtc + " -n " + ndx + " -b " + str(i) + " -e " + str(i+dt) + " -xvg none -res -o RMSF/" + prefix + "-" + str((i+dt)/1000) + "ns.xvg")

def tRMSF(ver,prefix,dt):

    f = open(prefix + ".rmsd.xvg","r")
    string = "text"
    string = f.readlines()[-1]
    line = string.strip('\n')
    time_ps = int(round(float(line.split()[0])))

    f = open(output, "w")
    line = 'text'

    dt2 = dt/1000
    time_ns = time_ps/1000
    for i in range(0,time_ns,dt2):
        r = open("RMSF/"+ prefix + "-"+str((i+dt2))+"ns.xvg", "r")
        line = "text"

        while True:
            line = r.readline()
            if not line: break
            if len(line.split()) > 0:
                res = str(line.split()[0]).ljust(8," ")
                rmsf = str(line.split()[1]).ljust(8," ")
                time = str(i+dt2).ljust(8, " ")

                f.write(time)
                f.write(res)
                f.write(rmsf)
                f.write("\n")
        f.write("\n")

    f.close()

def create_template():

    ###########################################
    f = open(prefix + ".rmsd.xvg","r")
    string = "text"
    string = f.readlines()[-1]
    line = string.strip('\n')
    time_ps = int(round(float(line.split()[0])))/1000

    r = open("RMSF/"+ prefix + "-1ns.xvg","r")
    string = "text"
    string = r.readlines()[-1]
    line = string.strip('\n')
    res = int(round(float(line.split()[0])))

    cont_time = "\nset xrange [1:" + str(time_ps) + "]"
    cont_res = "\nset yrange [0:" + str(res) + "]"
    #########################################

    template = open('template.gnu','w')

    content0 = "\nsplot '" + output + "'\n"

    content1 = """set pm3d map"""

    content2 = """
set cbrange [0.085:0.25]
set palette defined (0 "white",33 "#4169E1",66 "#F0E68C" ,100 "red")
#set palette defined (0 "blue",17 "#00ffff",33 "white",50 "yellow",66 "red",100 "#990000",101 "grey")
#set palette rgbformulae 22,13,10
#set palette maxcolor 4001
#set palette defined (0 "blue", 2000 "cyan", 2001 "gray", 2002 "yellow", 2400 "dark-yellow", 3000 "orange", 4000 "red")
#set palette maxcolor 1000
#set palette defined (0 "blue", 250 "cyan", 300 "green", 350 "yellow", 600 "dark-yellow", 999 "red")
set samples 10, 10
unset colorbox
set xtics out
set ytics out
set ztics out
set cbtics out
set mxtics 2
set mytics 2
set xtics font "Arial, 12"
set ytics font "Arial, 12"
set cbtics font "Arial, 12"
set xtics scale 1
set ytics scale 1
set cbtics scale 1
set ytics nomirror
set xtics nomirror
set ztics nomirror
set cbtics nomirror
set title "Heat Map"
set ylabel "Residues"
set ylabel font "Arial, 12"
set xlabel "Time (ns)"
set xlabel font "Arial, 12" """

    content3 = """set pm3d interpolate 3,3"""

    content4 = """set pm3d interpolate 3,3"""

    content5 = """set term postscript enhanced color
set output 'tRMSF-gnu.ps'
replot
"""

    template.write(content1)
    template.write(cont_time)
    template.write(cont_res)
    template.write(content2)
    template.write(content0)
    template.write(content3)
    template.write(content0)
    template.write(content4)
    template.write(content0)
    template.write(content5)
    template.close()

    print "\n####################################"
    print "\n>>> Load your 'template.gnu' in gnuplot to check your RMSF heat map."
    print "Output     = template.gnu\nDados      = "+ output + "\nGNU output = tRMSF-gnu.ps\n"

#############################
#calc(ver,prefix,dt)
#tRMSF(ver,prefix,dt)
create_template()
