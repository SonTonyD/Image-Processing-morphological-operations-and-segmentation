import math
import numpy as np

import module.basicSetOperation as bso

def dilation(image_matrix, SE):
    width, height = image_matrix.shape[0], image_matrix.shape[1]
    SEwidth, SEheight = SE.shape[0], SE.shape[1]

    #SE = bso.reflection(SE)

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

def erosion(image_matrix):
    pass

def opening(image_matrix):
    pass

def closing(image_matrix):
    pass

def hitOrMiss(image_matrix):
    pass
