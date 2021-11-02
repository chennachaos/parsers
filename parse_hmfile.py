#ioff()

import sys
import numpy as np


def parse_hmfile(ndim, npElem, MAIN_ELEM_TYPE_NUM, inputfilename, configfilename):
    
    #
    map_elem_nnodes = {1:2, 2:3, 3:4, 4:4, 5:8, 6:6, 7:5, 8:3, 9:6, 10:9, 11:10, 12:27, 13:18, 14:14, 15:1}

    # generate the name of the ouput file
    
    outputfilename = inputfilename.split(".")[0]+".mpap"

    # Open the file with read only permit
    infile  = open(inputfilename, "r")

    ###############################
    #
    # read the input file and count the nodes, elements, BCs etc.
    #
    ###############################

    nNode = 0
    nElem = 0
    nDBC  = 0
    nFBC  = 0
    nOutNodes = 0

    coords = []
    elemNodeConn = []
    DBCs = []

    for line in infile:
        if(line):
            if(line[0:4] == "GRID"):
                nNode += 1
                #print(line.split(","))
                subline = line.split(",")[3:-1]
                subline = [float(i) for i in subline]
                coords.append(subline)
            if( (line[0:6] == "CTRIA3") or (line[0:6] == "CTRIA6") or (line[0:6] == "CTETRA") or (line[0:5] == "CHEXA") ):
                nElem += 1
                #print(line)
                subline = line.split(",")[3:-1]
                #print(subline)
                subline = [int(i) for i in subline]
                elemNodeConn.append(subline)
            if(line[0:3] == "SPC"):
                print(line)
                subline = line.split(",")[2:-1]
                subline = [float(i) for i in subline]
                print(subline)
                if(int(subline[1]) == 12):
                    nDBC += 2
                    DBCs.append([subline[0], 1, subline[2]])
                    DBCs.append([subline[0], 2, subline[2]])
                elif(int(subline[1]) == 123):
                    nDBC += 3
                    DBCs.append([subline[0], 1, subline[2]])
                    DBCs.append([subline[0], 2, subline[2]])
                    DBCs.append([subline[0], 3, subline[2]])
                else:
                    nDBC += 1
                    DBCs.append([subline[0], subline[1], subline[2]])


    print(nNode)
    print(nElem)
    print(nDBC)
    #print(DBCs)
    DBCs.sort()
    print(DBCs)
    DBCs = [list(i) for i in set(tuple(i) for i in DBCs)]
    DBCs.sort()
    nDBC = len(DBCs)
    #print(DBCs)
    print(nDBC)

    indices_to_remove = list()
    # remove duplcates
    for i in range(len(DBCs)-1):
        val1 = DBCs[i]
        val2 = DBCs[i+1]
#        print(val1, val2)
        if(val1[0:2] == val2[0:2]):
            print("Matches")
            if( ( abs(val1[2]) > 1.0e-10) and ( abs(val2[2]) > 1.0e-10) ):
                print("Something wrong in the boundary conditions for node %d \n" % (val1[0]))
            if( abs(val1[2]) > 1.0e-10):
                indices_to_remove.append(i)
            else:
                indices_to_remove.append(i+1)

    infile.close()


    print(type(indices_to_remove))
    print(indices_to_remove)
    
    for index in sorted(indices_to_remove, reverse=True):
        del DBCs[index]

    nDBC = len(DBCs)
    print(nDBC)

    ###############################
    #
    # read the input file and write to the output file
    #
    ###############################

    infile  = open(inputfilename, "r")
    outfile = open(outputfilename, "w")

    # Header
    outfile.write("ndim      %d\n" % ndim)
    outfile.write("npElem    %d\n" % npElem)
    outfile.write("nNode     %d\n" % nNode)
    outfile.write("nElem     %d\n" % nElem)
    outfile.write("nDBC      %d\n" % nDBC)
    outfile.write("nFBC      %d\n" % nFBC)
    outfile.write("nOutNodes %d\n" % nOutNodes)

    outfile.write("nodes\n")
    if(ndim == 2):
        for ii in range(nNode):
            outfile.write("%10d \t %14.10f \t %14.10f \n" % ((ii+1), coords[ii][0], coords[ii][1]) )
    else:
        for ii in range(nNode):
            outfile.write("%10d \t %14.10f \t %14.10f \t %14.10f\n" % ((ii+1), coords[ii][0], coords[ii][1], coords[ii][2]) )

    outfile.write("elements\n")
    for ii in range(nElem):
        outfile.write("%10d \t %6d \t %2d \t %2d" % (ii+1, 1, 1, 1) )
        for jj in range(len(elemNodeConn[ii])):
            outfile.write(" \t %10d " % elemNodeConn[ii][jj] )
        outfile.write("\n")

    outfile.write("prescribed boundary conditions\n")
    for ii in range(nDBC):
        outfile.write("%10d \t %6d \t %14.10f\n" % (int(DBCs[ii][0]), int(DBCs[ii][1]), DBCs[ii][2]) )

    outfile.write("nodal forces\n")
    outfile.write("outputnodes")

    infile.close()
    outfile.close()

    return
######################################################


inputfilename = "LDC3D-Tet4-mesh1.fem"
inputfilename = "LDC3D-Hex8-mesh1.fem"
configfilename = "boundaries.cfg"

#if len(sys.argv) > 1:
#    inputfilename = sys.argv[1]
#
#if len(sys.argv) > 2:
#    configfilename = int(sys.argv[2])

MAIN_ELEM_TYPE_NUM = 4

parse_hmfile(3, 4, MAIN_ELEM_TYPE_NUM, inputfilename, configfilename)









