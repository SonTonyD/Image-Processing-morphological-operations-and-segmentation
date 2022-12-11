import math
from PIL import Image
import numpy as np
import module.morphologicalOperation as mop
import module.basicSetOperation as bso

SE3 = np.array([[True,True,True],[True,True,True],[True,True,True]])

def regionGrowing_v1(image_matrix, seed_coordinate, treshold):

    width, height = image_matrix.shape[0], image_matrix.shape[1]
    x_seed, y_seed = seed_coordinate
    region = np.array([[x_seed, y_seed]])


    #Initialize RegionImage and Boundaries_position
    boundaries_position = np.array([])
    somethingChange = True
    regionImage = np.full((width, height), False)
    regionImage[x_seed, y_seed] = True

    
    
    #If during one scan nothing is added to region, that mean that the region is fully define
    while somethingChange == True:
        #ResetFlag
        somethingChange = False
        
        #Build boundariesImage
        boundariesImage =  bso.difference(mop.dilation(regionImage, SE3), regionImage)
        

        #Reset boundaries position and update Region Image
        boundaries_position = np.array([[x_seed, y_seed]])
        for i in range(width):
            for j in range(height):
                if boundariesImage[i,j] == True:
                    boundaries_position = np.vstack((boundaries_position, [i,j]))
        
        for k in range(boundaries_position.shape[0]):
            i = boundaries_position[k,0]
            j = boundaries_position[k,1]
            if distanceBetweenPixels(image_matrix[i,j], image_matrix[x_seed, y_seed], "euclidian") < treshold and isExistInRegion(region, [i,j]) == False:
                region = np.vstack((region, [i,j]))
                regionImage[i,j] = True 
                somethingChange = True





        '''
        #Region Growing bloc
        for i in range(minXRange, maxXRange + 1):
            for j in range(minYRange, maxYRange + 1):
                #Check if we are outside of the image
                if minXRange >= 0 and maxXRange < width and minYRange > 0 and maxYRange < height:
                    if isPixelConnectedToPointRegion([i,j] , region, "8_Adjacency"):
                        if distanceBetweenPixels(image_matrix[i,j], image_matrix[x_seed, y_seed], "euclidian") < treshold and isExistInRegion(region, [i,j]) == False:
                            region = np.vstack((region, [i,j]))
                            somethingChange = True
                            minXRange, maxXRange, minYRange, maxYRange = getOptimalSearchRange(image_matrix, region)
        '''

    Image.fromarray(regionImage).show("New Image")
    return region

def regionGrowing_v2(image_matrix, seed_coordinate, treshold):

    width, height = image_matrix.shape[0], image_matrix.shape[1]
    x_seed, y_seed = seed_coordinate
    region = np.array([[x_seed, y_seed]])


    somethingChange = True
    minXRange, maxXRange, minYRange, maxYRange = getOptimalSearchRange(image_matrix, region)

    #If during one scan nothing is added to region, that mean that the region is fully define
    while somethingChange == True:
        #ResetFlag
        somethingChange = False
        #Region Growing bloc
        for i in range(minXRange, maxXRange + 1):
            for j in range(minYRange, maxYRange + 1):
                #Check if we are outside of the image
                if minXRange >= 0 and maxXRange < width and minYRange > 0 and maxYRange < height:
                    if isPixelConnectedToPointRegion([i,j] , region, "8_Adjacency"):
                        if distanceBetweenPixels(image_matrix[i,j], image_matrix[x_seed, y_seed], "euclidian") < treshold and isExistInRegion(region, [i,j]) == False:
                            region = np.vstack((region, [i,j]))
                            somethingChange = True
                            minXRange, maxXRange, minYRange, maxYRange = getOptimalSearchRange(image_matrix, region)
    return region

def regionGrowing_v3(image_matrix, seed_coordinate, treshold):

    width, height = image_matrix.shape[0], image_matrix.shape[1]
    x_seed, y_seed = seed_coordinate
    region = np.array([[x_seed, y_seed]])
    just_added_points = np.array([[x_seed, y_seed]])


    somethingChange = True
    minXRange, maxXRange, minYRange, maxYRange = getOptimalSearchRange(image_matrix, region)

    #If during one scan nothing is added to region, that mean that the region is fully define
    while somethingChange == True: 

        #ResetFlag
        somethingChange = False
        #Reset number of new point
        nb_new_points = 0

        #Region Growing bloc
        for i in range(minXRange, maxXRange + 1):
            for j in range(minYRange, maxYRange + 1):
                #Check if we are outside of the image
                if minXRange >= 0 and maxXRange < width and minYRange > 0 and maxYRange < height:
                    if isPixelConnectedToPointRegion([i,j] , just_added_points, "8_Adjacency"):
                        if distanceBetweenPixels(image_matrix[i,j], image_matrix[x_seed, y_seed], "euclidian") < treshold and isExistInRegion(region, [i,j]) == False:
                            nb_new_points  += 1
                            region = np.vstack((region, [i,j]))
                            just_added_points = np.vstack((just_added_points, [i,j]))
                            somethingChange = True
                            minXRange, maxXRange, minYRange, maxYRange = getOptimalSearchRange(image_matrix, region)
        #Remove points which are not on boundaries of the region
        just_added_points = just_added_points[-nb_new_points:]
    return region

def regionGrowing_v4(image_matrix, seed_coordinate, treshold):
    width, height = image_matrix.shape[0], image_matrix.shape[1]
    x_seed, y_seed = seed_coordinate
    region = np.array([[x_seed, y_seed]])
    just_added_points = np.array([[x_seed, y_seed]])


    somethingChange = True

    #If during one scan nothing is added to region, that mean that the region is fully define
    while somethingChange == True: 

        #ResetFlag
        somethingChange = False
        #Reset number of new point
        nb_new_points = 0

        #Region Growing bloc
        for point in just_added_points:
            i, j = point[0], point[1]
            for k in range(-1,2):
                for l in range(-1,2):
                    if i+k >= 0 and i+k < width and j+l > 0 and j+l < height:
                        if isPixelConnectedToPointRegion([i+k,j+l] , just_added_points, "8_Adjacency"):
                            if distanceBetweenPixels(image_matrix[i+k,j+l], image_matrix[x_seed, y_seed], "euclidian") < treshold and isExistInRegion(region, [i+k,j+l]) == False:
                                nb_new_points  += 1
                                region = np.vstack((region, [i+k,j+l]))
                                just_added_points = np.vstack((just_added_points, [i+k,j+l]))
                                somethingChange = True
        #Remove points which are not on boundaries of the region
        just_added_points = just_added_points[-nb_new_points:]
    return region

def regionGrowing_v5(image_matrix, seed_coordinate, treshold):
    width, height = image_matrix.shape[0], image_matrix.shape[1]
    x_seed, y_seed = seed_coordinate
    region = np.array([[x_seed, y_seed]])
    just_added_points = np.array([[x_seed, y_seed]])
    checked_points = np.full((width, height), False)


    somethingChange = True

    #If during one scan nothing is added to region, that mean that the region is fully define
    while somethingChange == True: 

        #ResetFlag
        somethingChange = False
        #Reset number of new point
        nb_new_points = 0

        #Region Growing bloc
        for point in just_added_points:
            i, j = point[0], point[1]
            for k in range(-1,2):
                for l in range(-1,2):
                    if i+k >= 0 and i+k < width and j+l > 0 and j+l < height:
                        if checked_points[i+k,j+l] == False:
                            if isPixelConnectedToPointRegion([i+k,j+l] , just_added_points, "8_Adjacency"):
                                if distanceBetweenPixels(image_matrix[i+k,j+l], image_matrix[x_seed, y_seed], "euclidian") < treshold and isExistInRegion(region, [i+k,j+l]) == False:
                                    nb_new_points  += 1
                                    region = np.vstack((region, [i+k,j+l]))
                                    just_added_points = np.vstack((just_added_points, [i+k,j+l]))
                                    somethingChange = True
                            #Say that this point is already checked, so we don't need to re-check it
                            checked_points[i+k,j+l] = True
        #Remove points which are not on boundaries of the region
        just_added_points = just_added_points[-nb_new_points:]
    return region


# Adjacency 8 neighborhood
def isPixelConnectedToPointRegion(currentPixelPosition, region, adjacencyType):
    if adjacencyType == "8_Adjacency":
        x_pixel, y_pixel = currentPixelPosition
        for i in range(x_pixel -1, x_pixel + 2):
            for j in range(y_pixel -1, y_pixel + 2):
                for k in range(region.shape[0]):
                    if i == region[k,0] and j == region[k,1]:
                        return True
        return False



# EuclidianDistance
def distanceBetweenPixels(pixelA, pixelB, distanceType):
    if distanceType == "euclidian":
        return abs(int(pixelB) - int(pixelA))

def isExistInRegion(region, currentPixelPosition):
    x_pixel, y_pixel = currentPixelPosition
    for i in range(region.shape[0]):
        if region[i,0] == x_pixel and region[i,1] == y_pixel:
            return True
    return False

def getOptimalSearchRange(image_matrix, region):
    width, height = image_matrix.shape[0], image_matrix.shape[1]
    minX,maxX,minY,maxY = width-2, 2, height-2, 2
    for i in range(region.shape[0]):
        if minX + 1 > region[i,0]:
            minX = region[i,0] - 1
        
        if maxX - 1 < region[i,0]:
            maxX = region[i,0] + 1
        
        if minY + 1> region[i,1]:
            minY = region[i,1] - 1
        
        if maxY - 1 < region[i,1]:
            maxY = region[i,1] + 1
    
    if minX < 0 +2:
        minX = 0 +2 
    if minY < 0 +2:
        minY = 0 +2 
    if maxX > width-2:
        maxX = width-2 
    if maxY > height-2:
        maxY = height-2 
    return minX,maxX,minY,maxY




def colorRegion(image_matrix, region, color_value):
    copy_image = np.copy(image_matrix)
    for k in range(region.shape[0]):
        copy_image[region[k,0], region[k,1]] = color_value
    return copy_image
            






'''
def regionGrowing(image_matrix, seed_location):
    #listOfRegion = initializeListOfRegion(seed_location)
    #mean_region_list = initializeRegionsMean(image_matrix, seed_location)
    #unallocated_pixels = seed_location

    for region in listOfRegion:
        for pixel in region:
'''



