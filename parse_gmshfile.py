#ioff()

import sys
import numpy as np


def parse_gmshfile(ndim, MAIN_ELEM_TYPE_NUM, inputfilename, configfilename):
    
    #
    map_elem_nnodes = {1:2, 2:3, 3:4, 4:4, 5:8, 6:6, 7:5, 8:3, 9:6, 10:9, 11:10, 12:27, 13:18, 14:14, 15:1}
    map_XYZ_nums = {"X":1, "Y":2, "Z":3, "E":4, "M":7}
    
    npElem = map_elem_nnodes[MAIN_ELEM_TYPE_NUM]

    # generate the name of the ouput file
    
    #outputfilename = inputfilename.split(".")[0]+".dat"
    outputfilename = "I"+inputfilename.split(".")[0]

    # Open the file with read only permit
    infile  = open(inputfilename, "r")
    outfile = open(outputfilename, "w")

    ###############################
    #
    # read the input file
    #
    ###############################

    # Header, 3 lines
    line = infile.readline()
    print(line)
    line = infile.readline()
    line = infile.readline()

    # PhysicalNames
    line = infile.readline()
    print(line)

    #assert (line == "$PhysicalNames")

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

    # Number of Nodes
    line = infile.readline()
    listtemp = " ".join(line.split())
    listtemp = listtemp.split(" ")
    nNode = int(listtemp[0])
    coords = np.zeros((nNode, ndim), dtype=float)
    for ii in range(nNode):
        line = infile.readline()
        listtemp = " ".join(line.split())
        listtemp = listtemp.split(" ")
        #print(listtemp)
        coords[ii,0] = float(listtemp[1])
        coords[ii,1] = float(listtemp[2])
        if(ndim == 3):
            coords[ii,2] = float(listtemp[3])

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
    elemNodeConn = np.zeros((nElemTotal, npElem), dtype=np.int32)
    elemVolNum   = np.zeros((nElemTotal, 1), dtype=np.int32)


    # list of nodes from the elements corresponding to the boundary physical groups
    # are stroed into lists first. Then, the unique node numbers of filtered out using 'set'
    PhysicalGroups_nodes = [[] for i in range(numPhysicalGroups)]

    nElem = 0
    for ii in range(nElemTotal):
        line = infile.readline()
        #print(line)
        listtemp = " ".join(line.split())
        listtemp = listtemp.split(" ")
        #print(listtemp)
        print(int(listtemp[3]))
        if(int(listtemp[1]) == MAIN_ELEM_TYPE_NUM):
            elemVolNum[nElem,0] = int(listtemp[4])
            for jj in range(map_elem_nnodes[int(listtemp[1])]):
                elemNodeConn[nElem,jj] = int(listtemp[5+jj])
            nElem += 1
        else:
            #print(map_elem_nnodes[int(listtemp[1])])
            for jj in range(map_elem_nnodes[int(listtemp[1])]):
                ind = PhysicalGroups_index.index(int(listtemp[3]))
                PhysicalGroups_nodes[ind].append(int(listtemp[5+jj]))

    # EndElements
    line = infile.readline()
    print(line)


    ###############################
    #
    # process boundary information
    #
    ###############################

    # find unique values in PhysicalGroups_nodes
    for ii in range(numPhysicalGroups):
        PhysicalGroups_nodes[ii] = list(set(PhysicalGroups_nodes[ii]))
        #print(PhysicalGroups_nodes[ii])

    print(len(PhysicalGroups_nodes))

    # open the configuration file containing the 
    # information for the boundary conditions
    # on the Physical groups
    #
    configfile  = open(configfilename, "r")
    DBCs = []

    while True:
        line = configfile.readline()

        if not line:
            break;
        
        #print(line)

        # check if the line contains ",".
        # if it does, then this line starts with the name of a physical group
        listtemp = " ".join(line.split())
        listtemp = listtemp.split(",")
        namestr = listtemp[0]
        numstr  = int(listtemp[1])

        print("PhysicalGroups_string.index(namestr)")
        print(PhysicalGroups_string.index(namestr))
        nodelisttemp = PhysicalGroups_nodes[PhysicalGroups_string.index(namestr)]

        for i in range(numstr):
            line = configfile.readline()
            print(line)
            line = line.replace(" ", "")
            print(line)
            listtemp = " ".join(line.split())
            listtemp = listtemp.split("->")
            print(listtemp)

            dof = map_XYZ_nums[listtemp[0]]
            #if(ndim == 2):
            #    dof -= 1
            specval = float(listtemp[1])
            print(dof,specval)

            for ii in range(len(nodelisttemp)):
                DBCs.append([nodelisttemp[ii], dof, specval])


    nDBC = len(DBCs)
    print(nDBC)
    #print(DBCs)
    DBCs.sort()
    #print(DBCs)
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
                indices_to_remove.append(i+1)
            else:
                indices_to_remove.append(i)

    print(type(indices_to_remove))
    print(indices_to_remove)
    
    for index in sorted(indices_to_remove, reverse=True):
        del DBCs[index]

    nDBC = len(DBCs)
    print(nDBC)


    ###############################
    #
    # write the output file
    #
    ###############################

    nFBC = 0
    nOutNodes = 0

    # for one pressure DOF
    #nDBC += 1

    # Header
    #outfile.write("ndim      %d\n" % ndim)
    #outfile.write("npElem    %d\n" % npElem)
    #outfile.write("nNode     %d\n" % nNode)
    #outfile.write("nElem     %d\n" % nElem)
    #outfile.write("nDBC      %d\n" % nDBC)
    #outfile.write("nFBC      %d\n" % nFBC)
    #outfile.write("nOutNodes %d\n" % nOutNodes)

    outfile.write("Dimension\n")
    outfile.write("%d\n\n\n\n" % ndim)

    outfile.write("\n\n\nNodes\n")
    outfile.write("%d\n" % nNode)
    if(ndim == 2):
        for ii in range(nNode):
          outfile.write("%d \t %14.10f \t %14.10f \n" % ((ii+1), coords[ii,0], coords[ii,1]) )
    else:
        for ii in range(nNode):
          outfile.write("%d \t %14.10f \t %14.10f \t %14.10f\n" % ((ii+1), coords[ii,0], coords[ii,1], coords[ii,2]) )

    outfile.write("\n\n\nElements\n")
    outfile.write("%d\n" % nElem)
    for ii in range(nElem):
        outfile.write("%10d \t %6d \t %2d \t %2d" % (ii+1, elemVolNum[ii,0], elemVolNum[ii,0], 1) )
        #outfile.write("%10d \t %6d \t %2d \t %2d" % (ii+1, 1, 1, 1) )
        for jj in range(len(elemNodeConn[ii])):
            outfile.write(" \t %10d " % elemNodeConn[ii][jj] )
        outfile.write("\n")

    outfile.write("\n\n\nPrescribed Boundary Conditions\n")
    outfile.write("%d\n" % nDBC)
    for ii in range(nDBC):
        outfile.write("%10d \t %6d \t %14.10f\n" % (int(DBCs[ii][0]), int(DBCs[ii][1]), DBCs[ii][2]) )
    #outfile.write("%10d \t %6d \t %14.10f\n" % (1, (ndim+1), 0.0) )

    #outfile.write("nodal forces\n")
    #outfile.write("outputnodes")

    infile.close()
    outfile.close()
    configfile.close()

    return
######################################################


inputfilename = "sphericalgripper.msh"
configfilename = "boundaries.cfg"
MAIN_ELEM_TYPE_NUM = 12

# Element type
#  9 ->  6-node Tria
# 10 ->  9-node Quad
#  5 ->  8-node Hexa
# 11 -> 10-node Tetra
# 12 -> 27-node Hexa
# 13 -> 18-node Wedge

if len(sys.argv) < 4:
    print("Enough number of input arguments not specified")
    print("Aborting the execution now...")
    print("Must enter <input-mesh-file(string)>  <boundary-config-file(string)> <element-type(int)>")
    sys.exit("aa! errors!")


inputfilename  = sys.argv[1]
configfilename = sys.argv[2]
MAIN_ELEM_TYPE_NUM = int(sys.argv[3])

ndim = 3
if( (MAIN_ELEM_TYPE_NUM == 10) or (MAIN_ELEM_TYPE_NUM == 9) ):
    ndim = 2


parse_gmshfile(ndim, MAIN_ELEM_TYPE_NUM, inputfilename, configfilename)









