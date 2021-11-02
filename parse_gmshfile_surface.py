#
# Parses .msh file generated using GMSH
#
# Creates an output file consisting of points and elements
# for immersed surfaces compatible with MPAP.
# This script is for 3D problems.
#
# Usage:
# python3  parse_gmshfile_surface.py  <file>.msh
#
# Output: <file>.mpap
#
# Author: Dr Chennakesava Kadapa
# Date: 31-Oct-2021
#
###############################################################


#ioff()

import sys
import numpy as np


def parse_gmshfile_surface(inputfilename):
    
    # generate the name of the ouput file
    
    outputfilename = inputfilename.split(".")[0]+".mpap"

    # Open the file with read only permit
    infile  = open(inputfilename, "r")
    outfile = open(outputfilename, "w")

    ###############################
    #
    # read the input file, 
    # process data and
    # write it to the output file
    #
    ###############################

    # Header, 3 lines
    line = infile.readline()
    print(line)
    line = infile.readline()
    line = infile.readline()
    print(line)

    # PhysicalNames
    line = infile.readline()
    print(line)
    #print("$PhysicalNames")

    assert line.strip() == "$PhysicalNames", "PhysicalNames are not present in the .msh file"

    # Number of PhysicalNames
    line = infile.readline()
    listtemp = " ".join(line.split())
    listtemp = listtemp.split(" ")
    numPhysicalGroups = int(listtemp[0])

    PhysicalGroups_index = []
    PhysicalGroups_string = []
    for ii in range(numPhysicalGroups):
        line = infile.readline()
        listtemp = " ".join(line.split())
        listtemp = listtemp.split(" ")
        #
        PhysicalGroups_index.append(int(listtemp[1]))
        PhysicalGroups_string.append(listtemp[2])

    print(PhysicalGroups_index)
    print(PhysicalGroups_string)

    # EndPhysicalNames
    line = infile.readline()
    print(line)

    # Nodes
    line = infile.readline()
    print(line)

    outfile.write("immersed points\n")

    # Number of Nodes
    line = infile.readline()
    listtemp = " ".join(line.split())
    listtemp = listtemp.split(" ")
    nNode = int(listtemp[0])

    for ii in range(nNode):
        line = infile.readline()
        listtemp = " ".join(line.split())
        listtemp = listtemp.split(" ")
        #
        #print(listtemp)
        # write points to the output file
        outfile.write("%d \t %14.10f \t %14.10f \t %14.10f\n" % (ii+1, float(listtemp[1]), float(listtemp[2]), float(listtemp[3]) ) )

    #
    # EndNodes
    line = infile.readline()
    print(line)

    # Elements
    line = infile.readline()
    print(line)

    # Number of Elements
    line = infile.readline()
    listtemp = " ".join(line.split())
    listtemp = listtemp.split(" ")
    nElemTotal = int(listtemp[0])


    outfile.write("\n\n\n\n")
    outfile.write("immersed integration elements\n")

    nElem = 0
    for ii in range(nElemTotal):
        line = infile.readline()
        #print(line)
        listtemp = " ".join(line.split())
        listtemp = listtemp.split(" ")
        #print(listtemp)
        #print(int(listtemp[1]))

        surface_number = int(listtemp[3])
        #print(int(listtemp[3]))            
        ind = PhysicalGroups_index.index(surface_number)
        #print(ind)

        act_inact_string = PhysicalGroups_string[ind]
        #print(act_inact_string)

        if(act_inact_string == '"active"'):
            act_inact_flag = 1
        else:
            act_inact_flag = 0

        if( int(listtemp[1]) == 3 ):
            outfile.write("%10d \t %2d \t %10d \t %10d \t %10d \t %10d\n" % (ii+1, act_inact_flag, int(listtemp[5]), int(listtemp[8]), int(listtemp[6]), int(listtemp[7])) )
            nElem += 1
        elif( int(listtemp[1]) == 2 ):
            outfile.write("%10d \t %2d \t %10d \t %10d \t %10d\n" % (ii+1, act_inact_flag, int(listtemp[5]), int(listtemp[6]), int(listtemp[7])) )
            nElem += 1

    # EndElements
    line = infile.readline()
    print(line)



    infile.close()
    outfile.close()

    return
######################################################



if len(sys.argv) < 1:
    print("Enough number of input arguments not specified")
    print("Aborting the execution now...")
    #print("Must enter <input-mesh-file(string)>  <boundary-config-file(string)> <element-type(int)>")
    print("Must enter <input-mesh-file(string)>  <boundary-config-file(string)>")
    sys.exit("aa! errors!")


inputfilename  = sys.argv[1]

parse_gmshfile_surface(inputfilename)









