import math
import numpy as np

import module.basicSetOperation as bso

#xi Structural Element
C1_hit = np.array([[True,False,False],[True,False,False],[True,False,False]])
C1_miss = np.array([[False,True,True],[False,False,True],[False,True,True]])
C1 = np.array([C1_hit,C1_miss])

C2_hit = np.array([[True,True,True],[False,False,False],[False,False,False]])
C2_miss = np.array([[False,False,False],[True,False,True],[True,True,True]])
C2 = np.array([C2_hit,C2_miss])

C3_hit = np.array([[False,False,True],[False,False,True],[False,False,True]])
C3_miss = np.array([[True,True,False],[True,False,False],[True,True,False]])
C3 = np.array([C3_hit,C3_miss])

C4_hit = np.array([[False,False,False],[False,False,False],[True,True,True]])
C4_miss = np.array([[True,True,True],[True,False,True],[False,False,False]])
C4 = np.array([C4_hit,C4_miss])

SE_xi = np.array([C1,C2,C3,C4])

#xii Structural Element
B1_hit = np.array([[False,False,False],[False,True,False],[True,True,True]])
B1_miss = np.array([[False,False,False],[True,False,True],[False,False,False]])
B1 = np.array([B1_hit,B1_miss])

B2_hit = np.array([[False,False,False],[True,True,False],[True,True,False]])
B2_miss = np.array([[True,False,False],[False,False,False],[False,False,True]])
B2 = np.array([B2_hit,B2_miss])

B3_hit = np.array([[True,False,False],[True,True,False],[True,False,False]])
B3_miss = np.array([[False,True,False],[False,False,False],[False,True,False]])
B3 = np.array([B3_hit,B3_miss])

B4_hit = np.array([[True,True,False],[True,True,False],[False,False,False]])
B4_miss = np.array([[False,False,True],[False,False,False],[True,False,False]])
B4 = np.array([B4_hit,B4_miss])

B5_hit = np.array([[True,True,True],[False,True,False],[False,False,False]])
B5_miss = np.array([[False,False,False],[True,False,True],[False,False,False]])
B5 = np.array([B5_hit,B5_miss])

B6_hit = np.array([[False,True,True],[False,True,True],[False,False,False]])
B6_miss = np.array([[True,False,False],[False,False,False],[False,False,True]])
B6 = np.array([B6_hit,B6_miss])

B7_hit = np.array([[False,False,True],[False,True,True],[False,False,True]])
B7_miss = np.array([[False,True,False],[False,False,False],[False,True,False]])
B7 = np.array([B7_hit,B7_miss])

B8_hit = np.array([[False,False,False],[False,True,True],[False,True,True]])
B8_miss = np.array([[False,False,True],[False,False,False],[True,False,False]])
B8 = np.array([B8_hit,B8_miss])

SE_xii = np.array([B1,B2,B3,B4,B5,B6,B7,B8])




def dilation(image_matrix, SE):
    width, height = image_matrix.shape[0], image_matrix.shape[1]
    SEwidth, SEheight = SE.shape[0], SE.shape[1]

    result = np.full((width, height), False)

    for i in range(1,width-1):
        for j in range(1,height-1):
            isIntersection = False
            for k in range(SEwidth):
                for l in range(SEheight):
                    if SE[k,l] == True and SE[k,l] == image_matrix[i-1+k,j-1+l]:
                        isIntersection = True
            if isIntersection == True:
                result[i,j] = True
    return result

def erosion(image_matrix, SE):
    width, height = image_matrix.shape[0], image_matrix.shape[1]
    SEwidth, SEheight = SE.shape[0], SE.shape[1]

    result = np.full((width, height), False)

    for i in range(1,width-1):
        for j in range(1,height-1):
            isInclude = True
            for k in range(SEwidth):
                for l in range(SEheight):
                    if SE[k,l] == True and SE[k,l] != image_matrix[i-1+k,j-1+l]:
                        isInclude = False
            if isInclude == True:
                result[i,j] = True
    return result

def opening(image_matrix, SE):
    return dilation(erosion(image_matrix, SE), SE) 

def closing(image_matrix, SE):
    return erosion(dilation(image_matrix, SE), SE) 

def HMT(image_matrix, SE_hit, SE_miss):
    element_1 = erosion(image_matrix, SE_hit)
    element_2 = erosion(bso.complement(image_matrix), SE_miss)
    return bso.intersection(element_1, element_2)



def super_M5_variant(image_matrix, SE_xii, index, super_index):
    if super_index == 0:
        return M5_variant(image_matrix, SE_xii, index)
    return super_M5_variant(M5_variant(image_matrix, SE_xii, index), SE_xii, index, super_index-1)


def M5_variant(image_matrix, SE_xii, index):
    if index == 0:
        return N_operation(image_matrix, SE_xii[index])
    return M5_variant(N_operation(image_matrix, SE_xii[index]), SE_xii, index-1)
        

def N_operation(image_matrix, SE_HMT):
    element_1 = bso.complement(HMT(image_matrix, SE_HMT[0], SE_HMT[1]))
    return bso.intersection(image_matrix, element_1)


