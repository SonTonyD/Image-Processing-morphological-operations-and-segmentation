from PIL import Image
import numpy as np
import click

import module.morphologicalOperation as mop
import module.basicSetOperation as bso

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
    
    
    #result = mop.dilation(image_matrix, SE1)
    result = mop.erosion(image_matrix, SE1)

    Image.fromarray(result).show("New Image")


if __name__ == '__main__':
    operation()
    

