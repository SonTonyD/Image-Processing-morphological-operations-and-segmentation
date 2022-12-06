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
def operation(name) :
    img = Image.open(name)
    image_matrix = np.array(img)
    Image.fromarray(image_matrix).show("New Image")

    SE1 = np.array([[False,False,False],[False,True,True],[False,False,False]])
    SE2 = np.array([[False,False,False],[False,True,False],[False,True,False]])
    SE3 = np.array([[True,True,True],[True,True,True],[True,True,True]])

    
    
    result = mop.dilation(image_matrix, SE1)
    #result = mop.erosion(image_matrix, SE1)
    #result = mop.opening(image_matrix, SE1)
    #result = mop.closing(image_matrix, SE1)

    #result = mop.HMT(image_matrix, SE_hit, SE_miss)

    '''
    index must be 7
    super_index is the number of M5_operation you want
    '''
    numberOfM5 = 1
    SE_INDEX_CONST = 7
    start = time.perf_counter()

    #result = mop.super_M5_variant(image_matrix, mop.SE_xii, SE_INDEX_CONST, numberOfM5)
    tmp = mop.M5_variant(image_matrix, mop.SE_xii, SE_INDEX_CONST)
    result = mop.M5_variant(tmp, mop.SE_xii, SE_INDEX_CONST)

    end = time.perf_counter()
    print(f"M5 Operation:  {end - start:0.4f} seconds")
    print("for",numberOfM5," repeats")



    

    Image.fromarray(result).show("New Image")


if __name__ == '__main__':
    operation()
    

