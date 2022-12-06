import math
import numpy as np

def complement(image_matrix):
    width, height = image_matrix.shape[0], image_matrix.shape[1]
    result = np.full((width, height), False)
    for i in range(width):
        for j in range(height):
            if image_matrix[i,j] == False:
                result[i,j] = True
    return result

def intersection(image_matrix_A, image_matrix_B):
    width, height = image_matrix_A.shape[0], image_matrix_A.shape[1]
    result = np.full((width, height), False)
    for i in range(width):
        for j in range(height):
            if image_matrix_A[i,j] == True and image_matrix_B[i,j] == True:
                result[i,j] = True
    return result

def sum(image_matrix_A, image_matrix_B):
    width, height = image_matrix_A.shape[0], image_matrix_A.shape[1]

    result = np.zeros((width, height))
    for i in range(width):
        for j in range(height):
            if image_matrix_A[i,j] == True or image_matrix_B[i,j] == True:
                result[i,j] = True
    return result

def reflection(image_matrix):
    width, height = image_matrix.shape[0], image_matrix.shape[1]
    for i in range(width):
        for j in range(height):
            image_matrix[i,j] = not image_matrix[i,j]
    return image_matrix

def translation(image_matrix, p):
    width, height = image_matrix.shape[0], image_matrix.shape[1]
    result = np.full((width, height), False)
    
    for i in range(width):
        for j in range(height):
            if i+p[0] < width and j+p[1] < height and image_matrix[i,j] == True:
                result[i+p[0], j+p[1]] = True
    return result
