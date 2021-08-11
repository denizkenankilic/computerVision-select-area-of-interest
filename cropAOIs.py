# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 12:29:53 2021

@author: deniz.kilic
"""
import os
from PIL import Image
import numpy as np
import sys

# Image folder that contains images which will be cropped
imageFolderPath = r'Image_Folder' # Edit here
# Image folder that for cropped images
croppedImageFolderPath = r'Image_Folder_Cropped' # Edit here

# Area of interest are for image cropping, it contains n number of tuples
# Format is (left, top, right, bottom)
# Left and top values are included but right and bottom values are not included for cropping
areaOfInterests = [(4352, 5403, 9028, 8521), (8303, 2494, 11087, 4935),
                   (1546, 4492, 4293, 7547), (3920, 1381, 7604, 4387)]
# Path for .txt file that will cover information of original and cropped images
txtName = os.path.basename(croppedImageFolderPath)

# Function that reads images in folder, crops them wrt given area of interests
# and save them as .bmp & .raw types. In .txt file created below, information of
# area of interests and original image can be found.
def crop_images(imageFolderPath, croppedImageFolderPath, areaOfInterests, formettedImageType, isRawStoringEnabled):
    # imageFolderPath: Folder path of images that will be cropped.
    # croppedImageFolderPath: Folder path for cropped images.
    # areaOfInterests: Coordinates (tuples) of n number of area of interests. Format is (left, top, right, bottom).
    # formettedImageType: It can be 'none', 'bmp', 'jpg', 'png' etc.
    # isRawStoringEnabled: It can be 'True' or 'False'.
    imageNames = os.listdir(imageFolderPath)
    imageNames = [os.path.join(imageFolderPath, images) for images in imageNames]
    if len(imageNames) > 0:
        orginalImage = Image.open(imageNames[0])
    else:
        print("Folder is empty! There is no image file to prepare cropped files.")
        sys.exit()
    orginalImageWidth, orginalImageHeight = orginalImage.size

    if not os.path.exists(croppedImageFolderPath):
        os.makedirs(croppedImageFolderPath)
    f = open(croppedImageFolderPath + '/' + txtName + '.txt', 'a')
    f.write('Original Image Size:' + ' ' + str(orginalImageHeight) + '(height)' + 'x' + str(orginalImageWidth) + '(width)' + '\n')

    for j in range(len(areaOfInterests)):

        subCroppedPath = croppedImageFolderPath + '\\' + 'AOI_' + str(j + 1)
        if not os.path.exists(subCroppedPath + '_' + formettedImageType) and not formettedImageType == 'none':
            os.makedirs(subCroppedPath + '_' + formettedImageType)
        if not os.path.exists(subCroppedPath + '_raw') and isRawStoringEnabled == True:
            os.makedirs(subCroppedPath + '_raw')

    for i in range(len(imageNames)):

        imageName = os.path.split(imageNames[i])
        imageReaded = Image.open(imageNames[i])
        imgNameWoExt, imgExtension = os.path.splitext(imageName[1])

        for j in range(len(areaOfInterests)):

            subCroppedPath = croppedImageFolderPath + '\\' + 'AOI_' + str(j + 1)

            imCrop = imageReaded.crop(areaOfInterests[j])  # cropped
            ImageWidth, ImageHeight = imCrop.size
            # if condition stands for not repeating same lines for all images
            if i == 0:
                f.write('AOI_' + str(j + 1) + ' ' + 'Coordinates' + ' ' + '(left, top, right, bottom):' + ' ' +
                        str(areaOfInterests[j][0]) + ', ' + str(areaOfInterests[j][1])
                        + ', ' + str(areaOfInterests[j][2] - 1) + ', ' + str(areaOfInterests[j][3] - 1) +
                        '\n' + 'AOI_' + str(j + 1) + ' ' + 'Size' + ' ' + '(height, width):' + ' ' + str(
                    ImageHeight) + ', '
                        + str(ImageWidth) + '\n')
            if not formettedImageType == 'none':
                imCrop.save(subCroppedPath + '_' + formettedImageType + '\\' + imgNameWoExt + '.' + formettedImageType)
            if isRawStoringEnabled == True:
                imCrop_raw = np.array(imCrop)
                imCrop_raw.tofile(subCroppedPath + '_raw' + '\\' + imgNameWoExt + '.raw')

crop_images(imageFolderPath, croppedImageFolderPath, areaOfInterests, 'bmp', True)
