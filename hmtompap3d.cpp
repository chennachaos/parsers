/*=========================================================================

Create triangulation for the base grid and perform 
subtriangulation for the cut-cells


=========================================================================*/

//#include "headersVTK.h"
#include "headersBasic.h"
//#include "DistFunctions.h"
//#include "DistFunctions3D.h"
//#include "utilfuns.h"
//#include "myGeomUtilities.h"
//#include <algorithm>

#include <sstream>
#include <string>
#include <stdlib.h>

using namespace std;
//using namespace myGeom;


//typedef float REAL;

typedef double REAL;



int main(int argc, char* argv[])
{
    if(argc == 0)
    {
      cerr << " Error in Input data " << endl;
      return 1;
    }

    cout << argv[1] << endl;

    std::string prefix(argv[1]);
    std::string extn1(".fem");
    std::string extn2(".mpap");
    std::string fnamein  = prefix+extn1;
    std::string fnameout = prefix+extn2;

    ifstream fin(fnamein);

    if(fin.fail())
    {
       cout << " Could not open the Output file" << endl;
       exit(1);
    }

    ofstream fout(fnameout);

    if(fout.fail())
    {
       cout << " Could not open the Output file" << endl;
       exit(1);
    }

    fout.setf(ios::fixed);
    fout.setf(ios::showpoint);
    fout.precision(8);

    string line;

    bool flag1=true, flag2=true, flag3=true, flag4=true;
    int ii=0, dd, ndof=3, nNode=0, nn;
    double  xx, yy, zz, val;
    //double  fact = 0.001;
    double  fact = 1.0;

    cout << "factor = " << fact << endl;

    vector<vector<double> >  node_coords;
    vector<double>  vecTempDbl(3);

    while(getline(fin,line))
    {
      //std::cout << line << std::endl;

      std::stringstream   linestream(line);
      std::string         value;
      vector<string>  stringlist;

      ii=0;
      while(getline(linestream,value,','))
      {
        //std::cout << value << '\t';

        stringlist.push_back(value);
      }

      if(stringlist[0] == "GRID")
      {
        if(flag1)
        {
          fout << "\n\n\nnodes" << endl;
          flag1=false;
        }
        fout << stringlist[1] << '\t' << stof(stringlist[3])*fact << '\t' << stof(stringlist[4])*fact << '\t' << stof(stringlist[5])*fact << endl;

        vecTempDbl[0] = stof(stringlist[3]);
        vecTempDbl[1] = stof(stringlist[4]);
        vecTempDbl[2] = stof(stringlist[5]);

        node_coords.push_back(vecTempDbl);

        nNode = node_coords.size()+1;
      }

      if(stringlist[0] == "CTETRA")
      {
        //cout << " size = " << stringlist.size() << endl;
        if(flag2)
        {
          fout << "\n\n\nelements" << endl;
          flag2=false;
        }
        // 4-noded tetrahedral element
        if( stringlist.size() == 8 )
        {
          fout << stringlist[1] << '\t' << 1 << '\t' << 1 << '\t' << 1 << '\t' ;
          fout << stringlist[3] << '\t' << stringlist[4] << '\t' << stringlist[5] << '\t' << stringlist[6] << endl;
        }
        // 10-noded tetrahedral element
        if( stringlist.size() == 10 )
        {
          fout << stringlist[1] << '\t' << 1 << '\t' << 1 << '\t' << 1 << '\t' ;
          fout << stringlist[3] << '\t' << stringlist[4] << '\t' << stringlist[5] << '\t' ;
          fout << stringlist[6] << '\t' << stringlist[7] << '\t' << stringlist[8] << '\t' ;


          getline(fin,line);
          //std::cout << line << std::endl;

          std::stringstream   linestream2(line);
          std::string         value2;
          vector<string>  stringlist2;

          ii=0;
          while(getline(linestream2,value2,','))
          {
            //std::cout << value << '\t';

            stringlist2.push_back(value2);
          }
          fout << stringlist2[1] << '\t' << stringlist2[2] << '\t' << stringlist2[3] << '\t' << stringlist2[4] << endl;
        }
      }

      if( (stringlist[0] == "CTRIA3") || (stringlist[0] == "CTRIA6") )
      {
        //cout << " size = " << stringlist.size() << endl;
        if(flag4)
        {
          fout << "\n\n\nface load elements" << endl;
          flag4=false;
        }
        // 3-noded triangular element face
        if( stringlist.size() == 7 )
        {
          fout << stringlist[1] << '\t' << 403 << '\t' << 3 << '\t' << 1 << '\t' << 0 << '\t' << 0 << '\t' ;
          fout << stringlist[3] << '\t' << stringlist[4] << '\t' << stringlist[5] << endl;
        }

        // 6-noded triangular element face
        if( stringlist.size() == 12 )
        {
          fout << stringlist[1] << '\t' << 602 << '\t' << 6 << '\t' << 1 << '\t' << 0 << '\t' << 0 << '\t' ;
          fout << stringlist[3] << '\t' << stringlist[4] << '\t' << stringlist[5] << '\t' ;
          fout << stringlist[6] << '\t' << stringlist[7] << '\t' << stringlist[8] << endl;
        }
      }


      if(stringlist[0] == "CHEXA")
      {
        //cout << " size = " << stringlist.size() << endl;
        if(flag2)
        {
          fout << "\n\n\nelements" << endl;
          flag2=false;
        }
        // 8-noded hexahedral element
        if( stringlist.size() == 10 )
        {
          fout << stringlist[1] << '\t' << stringlist[2] << '\t' << 1 << '\t' << 1 << '\t' ;
          fout << stringlist[3] << '\t' << stringlist[4] << '\t' << stringlist[5] << '\t' ;
          fout << stringlist[6] << '\t' << stringlist[7] << '\t' << stringlist[8] << '\t' ;


          getline(fin,line);
          //std::cout << line << std::endl;

          std::stringstream   linestream2(line);
          std::string         value2;
          vector<string>  stringlist2;

          ii=0;
          while(getline(linestream2,value2,','))
          {
            //std::cout << value << '\t';

            stringlist2.push_back(value2);
          }
          fout << stringlist2[1] << '\t' << stringlist2[2] << endl;
        }
      }

      if(stringlist[0] == "SPC")
      {
        if(flag3)
        {
          fout << "\n\n\nprescribed boundary conditions" << endl;
          flag3=false;
        }
        if(stringlist[3] == "1")
        {
          nn = stoi(stringlist[2])-1;

          xx = node_coords[nn][0];
          yy = node_coords[nn][1];
          zz = node_coords[nn][2];

          //if(xx < 0.0001)
          //{
            //val = 16.0*yy*zz*(0.41-yy)*(0.41-zz)/0.41/0.41/0.41/0.41;

            //cout << nn << '\t' << xx << '\t' << yy << '\t' << zz << endl;
            //cout << stringlist[2] << '\t' << 1 << '\t' << val << endl;
            //fout << stringlist[2] << '\t' << 1 << '\t' << val << endl;
          //}
          //else
          //{
            fout << stringlist[2] << '\t' << 1 << '\t' << stringlist[4] << endl;
          //}
        }
        else if(stringlist[3] == "2")
        {
          fout << stringlist[2] << '\t' << 2 << '\t' << stringlist[4] << endl;
        }
        else if(stringlist[3] == "3")
        {
          fout << stringlist[2] << '\t' << 3 << '\t' << stringlist[4] << endl;
        }
        else if(stringlist[3] == "4")
        {
          fout << stringlist[2] << '\t' << 4 << '\t' << stringlist[4] << endl;
        }
        else if(stringlist[3] == "12")
        {
          fout << stringlist[2] << '\t' << 1 << '\t' << 0.0 << endl;
          fout << stringlist[2] << '\t' << 2 << '\t' << 0.0 << endl;
        }
        else if(stringlist[3] == "123")
        {
          fout << stringlist[2] << '\t' << 1 << '\t' << 0.0 << endl;
          fout << stringlist[2] << '\t' << 2 << '\t' << 0.0 << endl;
          fout << stringlist[2] << '\t' << 3 << '\t' << 0.0 << endl;
        }
        else
        {
          cout << "Error in SPC ..." << endl;
          cout << "Program aborted ..." << endl;
          exit(-1);
        }
      }
      //std::cout << std::endl;
    }


    fin.close();
    fout.close();

    return 0;
}










