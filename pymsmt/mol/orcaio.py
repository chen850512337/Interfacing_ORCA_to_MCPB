"""
Module for writting a ORCA file and read the coordinates and force
constants from ORCA output file.

Author: Jinfeng Chen

"""

import numpy
import linecache
from pymsmt.exp import *
from pymsmt.mol.constants import B_TO_A

#------------------------------------------------------------------------------
#------------------------  Write ORCA input file  -----------------------------
#------------------------------------------------------------------------------

def write_orcaatm(gauatm, fname, signum=3):
    wf = open(fname, 'a')
    if signum == 3:
        print("%-6s   %8.3f %8.3f %8.3f" %(gauatm.element, \
                     gauatm.crdx, gauatm.crdy, gauatm.crdz), file=wf)
    elif signum == 4:
        print("%-6s   %9.4f %9.4f %9.4f" %(gauatm.element, \
                     gauatm.crdx, gauatm.crdy, gauatm.crdz), file=wf)
    wf.close()

def write_orca_optf(goptf, smchg, SpinNum, gatms, signum=3):
    """
    Geometry Optimization file
    may need care for output print level
    if similar keywords "Geom=PrintInputOrient" is needed in ORCA?
    ORCA 5 and greater has new grid deine
    """
    optf = open(goptf, 'w')
    print("%maxcore  1000", file=optf)
    print("%pal nprocs 2 end", file=optf)

    print("! B3LYP D3BJ 6-31G* Opt Freq", file=optf)

    print("*xyz %d %d" %(smchg, SpinNum), file=optf)
    optf.close()

    if signum == 3:
        for gatmi in gatms:
            write_orcaatm(gatmi, goptf)
    elif signum == 4:
        for gatmi in gatms:
            write_orcaatm(gatmi, goptf, 4)

    # for orca geometry block
    optf = open(goptf, 'a')
    print("*", file=optf)
    optf.close()



def write_orca_mkf(gmkf, lgchg, SpinNum, gatms, largeopt, signum=3):

    #MK RESP input file
    mkf = open(gmkf, 'w')
    print("%maxcore  1000", file=mkf)
    print("%pal nprocs 2 end", file=mkf)
    print("! B3LYP D3BJ 6-31G*", file=mkf)

    if largeopt == 1:
        print("!Opt", file=mkf)
        print(r"%geom optimizehydrogens true end", file=mkf)
    elif largeopt == 2:
        print("!Opt", file=mkf)

    print("*xyz %d %d" %(lgchg, SpinNum), file=mkf)
    mkf.close()
    

    if signum == 3:
        for gatmi in gatms:
            write_orcaatm(gatmi, gmkf)
    elif signum == 4:
        for gatmi in gatms:
            write_orcaatm(gatmi, gmkf, signum)

    mkf = open(gmkf, 'a')
    print("*", file=mkf)
    mkf.close()

#------------------------------------------------------------------------------
#-----------------------Read info from ORCA output file--------------------
#------------------------------------------------------------------------------

def get_crds_from_orca(fname:str, atnums:int) -> list:
    """
    ORCA optimization will results in a .xyz file, which contains the optimized
    geometry. Thus read from that file is enough.
    """
    crds = []

    fp = open(fname, 'r')
    n_atoms = int(fp.readline().strip())
    if n_atoms != atnums:
        raise pymsmtError(
            'The atom number in ORCA output are not consistent with '
            'the input atom number.'
        )
    
    # comment line
    fp.readline()

    for i in range(n_atoms):
        line = fp.readline().strip().split()[1:]
        for xyz in line:
            crds.append(float(xyz))

    fp.close()

    return crds


def get_matrix_from_orca(fname:str, msize:int):
    """
    Read Orca .hess output for Hessian matrix
    test 3 atoms, 5 atoms system
    """

    i = 0
    hasfc = 0
    with open(fname, 'r') as fp:
        for line in fp:
            i = i + 1
            if '$hessian' in line:
                hasfc = hasfc + 1
                beginl = i + 2
                break
            

    if hasfc == 0:
        raise pymsmtError(
            'There is no \'$hessian\' found in the hess file. '
            'Please check whether the ORCA jobs are finished normally, and '
            'whether you are using the correct hess file.'
        )
    
    # check the number of elements
    elenums2 = linecache.getline(fname, beginl - 1)
    if int(elenums2) != msize:
        raise pymsmtError('The atom number is not consistent with the'
                         'matrix size in fchk file.')

    n_rows = msize//5
    if msize%5 == 0:
        endl = beginl + msize*n_rows + n_rows - 1
    else:
        endl = beginl + msize*(n_rows + 1) + n_rows


    
    fcmatrix = numpy.zeros((msize, msize), dtype=float)
    
    print(f'beginl: {beginl}, endl: {endl}')
    for i in range(beginl, endl+1):
        # Because ORCA hess file has the row and column number before the data
        # we can use that to fill the matrix
        line = linecache.getline(fname, i)
        # check if the title line
        if (i - beginl) % (msize+1) == 0:
            icolumns = [int(icol) for icol in line.split()]
            #print(icolumns)
        else:
            #print(line.split())
            irow = int(line.split()[0])
            for icol in range(len(icolumns)):
                fcmatrix[irow][icolumns[icol]] = float(line.split()[icol+1])

    linecache.clearcache()
    return fcmatrix


def get_esp_from_orca(chgfile:str, espfitfile:str, espfile:str):
    """
    Because ORCA does not have ESP fitting function yet, we need Multiwfn for 
    ESP fitting, thus read thet ESP from Multiwfn output file.
    We need at least two input for this function:
    .chg file for the coordinates (Angstrom)
    .txt for the ESP center (Bohr)
    So coordinates need to be converted to Bohr!!!
    """

    #------------Coordinate List for the Atom and ESP Center--------------
    crdl1 = []
    crdl2 = []
    # read atom coordinates from .chg file
    with open(chgfile, 'r') as fp:
        for line in fp:
            x, y, z = line.strip().split()[1:4]
            crdl1.append([float(x)/B_TO_A, float(y)/B_TO_A, float(z)/B_TO_A])

    espl2 = []
    # read ESP center coordinates from .txt file
    with open(espfitfile, 'r') as fp:
        context = fp.readlines()
        nesp_points = int(context[0].strip())
        for i in range(1, nesp_points+1):
            line = context[i]
            x, y, z, esp = line.strip().split()
            crdl2.append([float(x), float(y), float(z)])
            espl2.append(float(esp))



    #----------------Check and print-----------------------
    if len(crdl2) != nesp_points or len(espl2) != nesp_points:
        raise pymsmtError("The number of ESP fitting points is inconsistent "
                          "between coordinate and ESP value!")
    
    with open(espfile, 'w') as w_espf:
        print("%5d%5d%5d" %(len(crdl1), len(crdl2), 0), file=w_espf)
        for i in range(0, len(crdl1)):
            crd = crdl1[i]
            print("%16s %15.7E %15.7E %15.7E" %(' ', crd[0], crd[1], crd[2]), file=w_espf)
        for i in range(0, len(crdl2)):
            crd = crdl2[i]
            esp = espl2[i]
            print("%16.7E %15.7E %15.7E %15.7E" %(esp, crd[0], crd[1], crd[2]), file=w_espf)
        w_espf.close()
