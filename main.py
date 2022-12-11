from PIL import Image
import numpy as np
import click
import time

import module.morphologicalOperation as mop
import module.basicSetOperation as bso
import module.segmentationOperation as seo

def saveResult(image_matrix, save_path):
    Image.fromarray(image_matrix).save(save_path)
    Image.fromarray(image_matrix).show("New Image")


@click.command()
@click.option('--name', default="lena.bmp", help='path of the image. Example:--name .\lenac.bmp  ')
@click.option('--dilation', default=-1, help='make dilation operation, select your structural element from 1 to 10, -2 if you want to do it for all SE')
@click.option('--erosion', default=-1, help='make erosion operation, select your structural element from 1 to 10, -2 if you want to do it for all SE')
@click.option('--opening', default=-1, help='make opening operation, select your structural element from 1 to 10, -2 if you want to do it for all SE')
@click.option('--closing', default=-1, help='make closing operation, select your structural element from 1 to 10, -2 if you want to do it for all SE')
@click.option('--hmt', default=-1, help='')
@click.option('--m5', default=-1, help='')
@click.option('--growing', is_flag=True , help='')
def operation(name, dilation, erosion, opening, closing, hmt, m5, growing) :
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

    if growing:
        '''
        x = np.arange(10, width, 100)
        y = np.arange(10, height, 100)
        region_list = np.array([])

        treshold = 2

        for i in x:
            for j in y:
                regionImg = seo.regionGrowing_v1(image_matrix, (i,j), treshold)
                region_list = np.vstack((region_list, regionImg))
        
        index = 0
        result = image_matrix
        for region in region_list:
            result = seo.colorRegion(result, region, 255-8*index)
            index += 1

        Image.fromarray(result).save("./results/mono_region_growing.bmp")
        Image.fromarray(result).show("New Image")

        '''
        start = time.perf_counter()
        #ImgRegion = seo.regionGrowing_v1(image_matrix, (116,377), 25) # 226 seconds
        #ImgRegion = seo.regionGrowing_v2(image_matrix, (116,377), 25) # 12 seconds
        ImgRegion = seo.regionGrowing_v3(image_matrix, (16,450), 15) # 1.3 seconds
        result = seo.colorRegion(image_matrix, ImgRegion, 255)

        end = time.perf_counter()
        print(f"Region Growing:  {end - start:0.4f} seconds")

        Image.fromarray(result).save("./results/mono_region_growing.bmp")
        Image.fromarray(result).show("New Image")
        



    

    


if __name__ == '__main__':
    operation()
    

