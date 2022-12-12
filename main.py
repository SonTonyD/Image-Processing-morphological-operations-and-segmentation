from PIL import Image
import numpy as np
import click
import time
import re

import module.morphologicalOperation as mop
import module.basicSetOperation as bso
import module.segmentationOperation as seo

def saveResult(image_matrix, save_path):
    Image.fromarray(image_matrix).save(save_path)
    Image.fromarray(image_matrix).show("New Image")

def nameParsing(name):
    regex = re.compile(r'(?!images\b)\b(?!bmp\b)\b\w+')
    newName = regex.search(name).group()
    return newName


@click.command()
@click.option('--name', default="lena.bmp", help='path of the image. Example:--name .\lenac.bmp  ')
@click.option('--dilation', default=-1, help='make dilation operation, select your structural element from 1 to 10, -2 if you want to do it for all SE')
@click.option('--erosion', default=-1, help='make erosion operation, select your structural element from 1 to 10, -2 if you want to do it for all SE')
@click.option('--opening', default=-1, help='make opening operation, select your structural element from 1 to 10, -2 if you want to do it for all SE')
@click.option('--closing', default=-1, help='make closing operation, select your structural element from 1 to 10, -2 if you want to do it for all SE')
@click.option('--hmt', default=-1, help='')
@click.option('--m5', default=-1, help='')
@click.option('--growing', nargs=5, type=int , help=' region growing, parameters x_seed, y_seed, threshold, colorationType = 0 (boundaries) or 1 (region), homogeneity criteria (0 difference with the intensity of seed pixel, 1 difference with mean of the intensity of the region)')
@click.option('--merging', nargs=2, type=int , help=' merging region, parameters grid_gap, threshold')
def operation(name, dilation, erosion, opening, closing, hmt, m5, growing, merging) :
    img = Image.open(name)
    image_matrix = np.array(img)
    width, height = image_matrix.shape[0], image_matrix.shape[1]
    Image.fromarray(image_matrix).show("New Image")

    SE1 = np.array([[False,False,False],[False,True,True],[False,False,False]])
    SE2 = np.array([[False,False,False],[False,True,False],[False,True,False]])
    SE3 = np.array([[True,True,True],[True,True,True],[True,True,True]])
    SE4 = np.array([[False,True,False],[True,True,True],[False,True,False]])
    SE5 = np.array([[False,False,False],[False,True,True],[False,True,False]])
    SE6 = np.array([[False,False,False],[False,False,True],[False,True,False]])
    SE7 = np.array([[False,False,False],[True,True,True],[False,False,False]])
    SE8 = np.array([[False,False,False],[True,False,True],[False,False,False]])
    SE9 = np.array([[False,False,False],[True,True,False],[True,False,False]])
    SE10 = np.array([[False,True,True],[False,True,False],[False,False,False]])

    SE_group = np.array([SE1,SE2,SE3,SE4,SE5,SE6,SE7,SE8,SE9,SE10])

    if dilation != -1:
        if dilation == -2:
            for i in range(10):
                result = mop.dilation(image_matrix, SE_group[i])
                Image.fromarray(result).save("./results/dilation_SE"+str(i+1)+".bmp")
        else:
            result = mop.dilation(image_matrix, SE_group[dilation-1])
            Image.fromarray(result).save("./results/dilation_SE"+str(dilation)+".bmp")
            Image.fromarray(result).show("New Image")

    if erosion != -1:
        if erosion == -2:
            for i in range(10):
                result = mop.erosion(image_matrix, SE_group[i])
                Image.fromarray(result).save("./results/erosion_SE"+str(i+1)+".bmp")
        else:
            result = mop.erosion(image_matrix, SE_group[erosion-1])
            Image.fromarray(result).save("./results/erosion_SE"+str(erosion)+".bmp")
            Image.fromarray(result).show("New Image")
    
    if opening != -1:
        if opening == -2:
            for i in range(10):
                result = mop.opening(image_matrix, SE_group[i])
                Image.fromarray(result).save("./results/opening_SE"+str(i+1)+".bmp")
        else:
            result = mop.opening(image_matrix, SE_group[opening-1])
            Image.fromarray(result).save("./results/opening_SE"+str(opening)+".bmp")
            Image.fromarray(result).show("New Image")

    if closing != -1:
        if closing == -2:
            for i in range(10):
                result = mop.closing(image_matrix, SE_group[i])
                Image.fromarray(result).save("./results/closing_SE"+str(i+1)+".bmp")
        else:
            result = mop.closing(image_matrix, SE_group[closing-1])
            Image.fromarray(result).save("./results/closing_SE"+str(closing)+".bmp")
            Image.fromarray(result).show("New Image")

    if hmt != -1:
        if hmt == -2:
            for i in range(4):
                result = mop.HMT(image_matrix, mop.SE_xi[i][0], mop.SE_xi[i][1])
                Image.fromarray(result).save("./results/hmt_SE"+str(i+1)+".bmp")
        else:
            result = mop.HMT(image_matrix, mop.SE_xi[hmt-1][0], mop.SE_xi[hmt-1][1])
            Image.fromarray(result).save("./results/hmt_SE"+str(hmt)+".bmp")
            Image.fromarray(result).show("New Image")
    


    if m5 != -1:
        numberOfM5 = m5 - 1
        SE_INDEX_CONST = 7
        start = time.perf_counter()

        result = mop.super_M5_variant(image_matrix, mop.SE_xii, SE_INDEX_CONST, numberOfM5)
        end = time.perf_counter()
        print(f"M5 Operation:  {end - start:0.4f} seconds")
        print("for",numberOfM5+1," repeats")

        Image.fromarray(result).save("./results/m5_with_"+str(m5)+"_repeat.bmp")

    if len(growing) != 0:
        start = time.perf_counter()
        #SMALL REGION
        #ImgRegion = seo.regionGrowing_v1(image_matrix, (116,377), 25) # 226 seconds
        #ImgRegion = seo.regionGrowing_v2(image_matrix, (116,377), 25) # 12 seconds
        #ImgRegion = seo.regionGrowing_v3(image_matrix, (116,377), 25) # 1.3 seconds

        #MEDIUM REGION
        #ImgRegion = seo.regionGrowing_v3(image_matrix, (16,450), 15) # 12 seconds
        #ImgRegion = seo.regionGrowing_v4(image_matrix, (16,450), 15) # 10 seconds
        #ImgRegion = seo.regionGrowing_v5(image_matrix, (16,450), 15) # 0.66 seconds

        #LARGE REGION
        #ImgRegion = seo.regionGrowing_v3(image_matrix, (162,46), 15) # 514 seconds
        #ImgRegion = seo.regionGrowing_v4(image_matrix, (162,46), 15) # 125 seconds
        #ImgRegion = seo.regionGrowing_v5(image_matrix, (162,46), 15) #  15 seconds

        #VERY LARGE REGION
        #ImgRegion = seo.regionGrowing_v5(image_matrix, (38,100), 15) #  15 seconds

        x_seed = growing[0]
        y_seed = growing[1]
        threshold = growing[2]
        coloration = growing[3]
        homogeneity_criteria = growing[4]

        

        #ImgRegion = seo.regionGrowing_v5(image_matrix, (x_seed, y_seed), threshold)
        ImgRegion = seo.regionGrowing_v6(image_matrix, (x_seed, y_seed), threshold, homogeneity_criteria)
        
        if coloration == 0:
            result = seo.colorRegion(image_matrix, ImgRegion, 255)
        if coloration == 1:
            result = seo.colorBoundaries(image_matrix, ImgRegion, 255)
        if coloration == 2:
            result = seo.colorBoundariesEmptyImage(image_matrix, ImgRegion)
        

        end = time.perf_counter()
        print(f"Region Growing:  {end - start:0.4f} seconds")

        name = nameParsing(name)
        label = "_"+str(name)+"_"+str(x_seed)+"_"+str(y_seed)+"_"+str(threshold)+"_"+str(coloration)+"_"
        Image.fromarray(result).save("./results/region_growing"+label+".bmp")
        Image.fromarray(result).show("New Image")
    
    if len(merging) != 0:
        grid_gap = merging[0]
        threshold = merging[1]

        start = time.perf_counter()
        result = seo.mergeRegion(image_matrix, threshold, grid_gap) # 175 seconds

        end = time.perf_counter()
        print(f"Merge Region:  {end - start:0.4f} seconds")

        name = nameParsing(name)
        label = "_"+str(name)+"_"+str(grid_gap)+"_"+str(threshold)+"_"
        Image.fromarray(result).save("./results/region_merging"+label+".bmp")
        Image.fromarray(result).show("New Image")
        



    

    


if __name__ == '__main__':
    operation()
    

