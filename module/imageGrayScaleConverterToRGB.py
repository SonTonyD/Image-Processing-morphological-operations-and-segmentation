from PIL import Image
import numpy as np


def convertToRGB(image_matrix):
    width, height = image_matrix.shape[0], image_matrix.shape[1]

    img_rgb = Image.open("./images/lenac.bmp")
    image_matrix_model = np.array(img_rgb)

    image_matrix_rgb = np.zeros_like(image_matrix_model)

    for i in range(width):
        for j in range(height):
            for k in range(3):
                image_matrix_rgb[i,j,k] = image_matrix[i,j]

    return image_matrix_rgb



