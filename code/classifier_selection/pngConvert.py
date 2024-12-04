import cv2
import numpy as np
import pandas as pd
from utilities import stripFilesName

IMAGE_HEIGHT= 160
IMAGE_WIDTH= 240
FEATURES_AFTER_IMAGE_SIZE_REDUCTION= ((int(0.9*IMAGE_HEIGHT)-int(0.15*IMAGE_HEIGHT))      # Image height
                                      * (int(0.82*IMAGE_WIDTH)-int(0.2*IMAGE_WIDTH))      # Image width
                                      * 3)                                                # RGB 3 values per pixel

def png2csv(pngImg, csvFile):
    ''' This function converts a png image into a csv file

        Arguments:
            - The path to the png image
            - The path to an existing csv file
        
        The initial png image is a voronoi diagram
        The csv outpout format is used to train and test the model '''
    
    img= cv2.imread(pngImg)                                                     # Read the voronoi diagram as a png image
    img= cv2.resize(img, (IMAGE_WIDTH,IMAGE_HEIGHT))                            # Give the image a smaller size
    img= img[int(0.15*IMAGE_HEIGHT):int(0.9 * IMAGE_HEIGHT), 
             int(0.2 * IMAGE_WIDTH):int(0.82 * IMAGE_WIDTH)]
    img= img.flatten()                                                          # Convert the image into an one dimensional array
    fileName= stripFilesName(pngImg)                                            # Take the file's name without hierarchy folders above (path)
    img= np.append(img,fileName[0]).reshape(1, FEATURES_AFTER_IMAGE_SIZE_REDUCTION+1)                     # Add the category (label)(0-5) as the last value of the array
    pd.DataFrame(img).to_csv(csvFile, mode='a', header=False, index=False)      # Insert the numeric array as a new line into a csv file

def png2ndarray (pathToPng):
    '''Converts a png into a flatten 1-darray, label value not included'''

    ndArray= cv2.imread(pathToPng)                                              # Read the voronoi diagram as a png image
    ndArray= cv2.resize(ndArray, (IMAGE_WIDTH,IMAGE_HEIGHT))                            # Give the image a smaller size
    ndArray= ndArray[int(0.15*IMAGE_HEIGHT):int(0.9 * IMAGE_HEIGHT), 
             int(0.2 * IMAGE_WIDTH):int(0.82 * IMAGE_WIDTH)]
    ndArray= ndArray.flatten()                                                          # Convert the image into an one dimensional array
    return ndArray

