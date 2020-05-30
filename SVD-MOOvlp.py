#!/usr/bin/python
# coding: utf-8

# This program extract MO matrices from fchk or fmat files and calculate SVD
import math
import cmath
import numpy as np
np.set_printoptions(suppress=True)
from numpy import array
from numpy import diag
from numpy import dot
from numpy import zeros
import sys
##########
if len(sys.argv) < 5 or  len(sys.argv) > 5 :
    print('You need  5 arguments: name of the file, 1st filname, "1/-1 for Alpha or Beta' 
           ', 2nd filename, and "1/-1 for Alpha or Beta"')
    sys.exit(0)
####                
# This function will grab NBasis 
def NBasGrab(filename):
    NBasis = 0
    with open(filename, 'r') as f:
        if filename.endswith('.fmat'):
            for line in f:
                if "NBasis" in line:
                    words = line.split()
                    for i in words:
                        NBasis = int(words[3])
        elif filename.endswith('.fchk'):
            for line in f:
                if "Number of basis functions" in line:
                    words = line.split()
                    NBasis = int(words[5])
#            print (NBasis)                        
        else:
            print('The file extension is not supported. This script only supports fchk and fmat.')

    return NBasis

# This function will grab the Alpha or Beta MO Matrix 
def MatGrab(filename,switch):
#   Get number of basis functions    
    NBasis=NBasGrab(filename)
#################################    
    with open(filename,'r') as f:
#       FMAT FILES
        if filename.endswith('.fmat'):
#           Initializing variables for fmat file    
            Exlines = int(math.ceil(NBasis/5))
            MOlines =int(Exlines+(NBasis*Exlines))
            MOlista=[]
            MOlistb=[]
            MOFull=[]
            MOA=[]
            MOB=[]            
            if (switch == 1):                
#           Extract Alpha MO coefficient                
                for line  in f:
                    if  "ALPHA MO COEFFICIENTS" in line:
                        for m in range(0,MOlines):
                            nextline = next(f)
                            nextline = nextline.split()
                            MOlista.append(nextline)       
#                       Clean header rows and columns
                        for n in range(0,len(MOlista)-Exlines,NBasis):
                            del MOlista[n] 
                        for n in range(len(MOlista)):
                            del MOlista[n][0]

#                       For NBasis > 5, the matrix is stored in chunks. temp is equal to the number chunks.
                        temp=int((len(MOlista)/NBasis))
#        
#                       Create a copy of the first chunk of the matrix which is equal to NBasis.   
#                       Start filling the empty list "MOFull"                    
                        for i in range(0,NBasis):
                            MOFull.append(MOlista[i])                            
#                         
#                       "Extend" the list "MOFull" by the chunks left to match the NBasis x NBasis matrix
                        for k in range(1,temp+1):
                            for j in range(0,NBasis):
                                for i in range(len(MOlista)):
                                    if i==j+(NBasis*k):
                                        MOFull[j].extend(MOlista[i])                    
#               Concatenate the list into one array    
                ConcMOFull = np.array(np.concatenate([np.array(i) for i in MOFull]))
#               Create another list to "float" all the elements 
                for item in ConcMOFull:
                    MOA.append(float(item))
#               Reshape the matrix into NBasis by NBasis           
                MOCoeffA = np.reshape(MOA,(NBasis,NBasis))
#               Return  MOCoeffA
                return MOCoeffA
        #
            elif (switch == -1):
#           Extract Beta MO coefficient                
                for line  in f:
                    if  "BETA MO COEFFICIENTS" in line:
                        for m in range(0,MOlines):
                            nextline = next(f)
                            nextline = nextline.split()
                            MOlistb.append(nextline)     
        #                   Clean header rows and columns                        
                        for n in range(0,len(MOlistb)-Exlines,NBasis):
                            del MOlistb[n] 
                        for n in range(len(MOlistb)):
                            del MOlistb[n][0]
        #                   For NBasis > 5, the matrix is stored in chunks. temp is equal to the number chunks.
                        temp=int((len(MOlistb)/NBasis))
        #    
        #                   Create a copy of the first chunk of the matrix which is equal to NBasis.   
        #                   Start filling the empty list "MOFull"                    
                        for i in range(0,NBasis):
                            MOFull.append(MOlistb[i])                            
        #            
        #                   "Extend" the list "MOFull" by the chunks left to match the NBasis x NBasis matrix
                        for k in range(1,temp+1):
                            for j in range(0,NBasis):
                                for i in range(len(MOlistb)):
                                    if i==j+(NBasis*k):
                                        MOFull[j].extend(MOlistb[i])                    
        #           Concatenate the list into one array    
                ConcMOFull = np.array(np.concatenate([np.array(i) for i in MOFull]))
        #           Create another list to "float" all the elements 
                for item in ConcMOFull:
                    MOB.append(float(item))
        #           Reshape the matrix into NBasis by NBasis           
                MOCoeffB = np.reshape(MOB,(NBasis,NBasis))
        #       
                return MOCoeffB
######################################################################################################################
######################################################################################################################
#       FCHK FILES
        elif filename.endswith('.fchk'):
            MOElements = NBasis * NBasis
            MOlines = int(MOElements/5) + 1
            MOlista=[]
            MOlistb=[]
            MOA=[]
            MOB=[]         
            if (NBasis%5 == 0):
                MOlines = MOlines - 1
#           Extract Alpha MO coefficient  
            if (switch == 1):
                with open(filename,'r') as f:
                    for line  in f:
                        if  "Alpha MO coefficients" in line:
                            for m in range(0,MOlines):
                                nextline = next(f)
                                nextline = nextline.split()
#                                 print(nextline)
                                MOlista.extend((nextline))
#               Convert the items in the list to float
                for i in MOlista:
                    MOA.append(float(i))
#                 print(MOA)
#               Reshape the array into NBasis by NBasis matrix            
                MOCoeffA = np.reshape(np.array(MOA),(NBasis,NBasis),order='F')
#                 print(MOCoeffA)

                return MOCoeffA
#           Beta Case            
            if (switch == -1):
#           Extract Beta MO coefficient                
                with open(filename,'r') as f:
                    for line  in f:
                        if  "Beta MO coefficients" in line:
                            for m in range(0,MOlines):
                                nextline = next(f)
                                nextline = nextline.split()
#                                 print(nextline)
                                MOlistb.extend((nextline))
                for i in MOlistb:
                    MOB.append(float(i))
#               Reshape the array into NBasis by NBasis matrix            
                MOCoeffB = np.reshape(np.array(MOB),(NBasis,NBasis),order='F')

                return MOCoeffB
            
        else:
            print('The file extension is not supported. This script only supports fchk and fmat.')
########################            

#######################
##### AO OVERLAP ######
#######################
def FrmAOOverlap(A):
    CInv = np.linalg.inv(A)
    S = np.dot(np.transpose(CInv),CInv)
    return S

#######################
#####Sanity Checks#####
#######################
#MOCoeff =(MatGrab('H2.fmat',1))
#MOCoeffT=np.transpose(MOCoeff)
#AOOverlap=FrmAOOverlap(MatGrab("H2O.fmat",1))
#print ("MOCoeff")
#print (MOCoeff)
#print ("AO Overlap")
#print (AOOverlap)
## You should get IDENTITY matrix 
#print ("CT.AOS.C")
#print((np.matmul(np.matmul((MOCoeffT),AOOverlapfc),MOCoeff)))

#########################################
######## EXAMPLE on H2 MOLECULE #########
#########################################
#
# Pulling the Coeff. from the first file
filename =sys.argv[1]
switch = int( sys.argv[2])
# you can hhave different files, but they should have same dimensions
filename2 = sys.argv[3]
switch2 =  int(sys.argv[4])

MOCoeff1 = MatGrab(filename,switch)
#
# Pulling the Coeff. from the Second file
MOCoeff2 = MatGrab(filename2,switch2)
#
# Printing the coeff 
print("###############################")
print("### MO COEFF. OF",filename,"###")
print("###############################")
#print(" MOCoeff. of ",filename)
print(MOCoeff1)
print("")
# Printing the coeff
print("###############################")
print("### MO COEFF. OF",filename2,"###")
print("###############################")
#print(" MOCoeff. of ",filename2)
print(MOCoeff2)
print("")

# Calculate the overlap between the two MOCoeffs. with and without the AO overlap
MOOverlap  = np.matmul(np.transpose(MOCoeff1),MOCoeff2)

AOOverlap=FrmAOOverlap(MatGrab(filename,switch))

#MOOverlapS = np.matmul(np.matmul(np.transpose(MOCoeff1),AOOverlap),MOCoeff)
#
# Optional printing - uncomment it if needed
#print(" MO Overlap is ", MOOverlap)

######################################
###########CALCULATING SVD############
######################################

#      A = U * SIGMA * VT
#      VT = transpose(V)
#      where SIGMA is an M-by-N  diagonal matrix i.e is zero except for its
#      min(m,n) diagonal elements, U is an M-by-M orthogonal matrix, and
#      V is an N-by-N orthogonal matrix.  The diagonal elements of SIGMA
#      are the singular values of A; they are real and non-negative, and
#      are returned in descending order.  The first min(m,n) columns of
#      U and V are the left and right singular vectors of A.
# SVD
print("#########################################")
print("###CALCULATING SVD USING MO-MO OVERLAP###")
print("#########################################")
print("")
U, s, VT = np.linalg.svd(MOOverlap)
print("######################")
print("###### U MATRIX ######")
print("######################")
print(U)
print("")
print("#############################")
print("### SIGMA DIAGONAL MATRIX ###")
print("#############################")
print(diag(s))
print("")
print("##########################")
print("### V-TRANSPOSE MATRIX ###")
print("##########################")
print(VT)
print("")
print("################")
print("### V MATRIX ###")
print("################")
print(np.transpose(VT))
print("")

# We can also reconstruct the matrix using the diagonal matrix
# First, form the diagonal matrix from s
Sigma = diag(s)
#print("sigma" ,Sigma)
#print("")

# Reconstruct the initial matrix
Reconstructed_MOOverlap = U.dot(Sigma.dot(VT))

#print("Reconstructed_MOOverlap", Reconstructed_MOOverlap)
#print(" ")
#print("MOOverlap is", MOOverlap)




