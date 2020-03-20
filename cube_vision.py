'''
reference:
    1. Morphological processing
    -> https://blog.csdn.net/sunny2038/article/details/9137759
    -> https://www.jianshu.com/p/dcecaf62da71

    2. color spaces and color segmentation
    -> https://www.learnopencv.com/color-spaces-in-opencv-cpp-python/
    -> https://blog.csdn.net/hjxu2016/article/details/77834599

    3. find contours
    -> https://blog.csdn.net/sunny2038/article/details/12889059

    4. get extreme points in contours
    -> https://www.pyimagesearch.com/2016/04/11/finding-extreme-points-in-contours-with-opencv/

    5. hsv color filter
    -> https://github.com/alkasm/colorfilters/blob/master/colorfilters/__init__.py

questions:
    1. why should we convert input image from bgr to hsv ?
    -> https://www.learnopencv.com/color-spaces-in-opencv-cpp-python/
'''

import cv2
import numpy as np
import setting


# Color threshold to find the squares
open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))


def straighten(contours: list) -> tuple:

    ''' 
        find the left-top and the right-bottom in every contour(a group of points).

        x1,y1 ------
        |          |
        |          |
        |          |
        --------x2,y2

        input:
            a list of contours

        output:
            a list of rectangles :[
                ((x1, y1), (x2, y2)),
                ((x1, y1), (x2, y2)),
                ((x1, y1), (x2, y2)),
                ...
            ]
    '''

    rects = []
    for cont in contours:

        left = tuple(cont[:,0][cont[:,:,0].argmin()])
        right = tuple(cont[:,0][cont[:,:,0].argmax()])
        top = tuple(cont[:,0][cont[:,:,1].argmin()])
        bottom = tuple(cont[:,0][cont[:,:,1].argmax()])

        # add left-top and right-bottom points
        rects.append(((left[0], top[1]), (right[0], bottom[1])))

    return rects

def sort_coordinate(grids: dict) ->list:

    ''' 
        sort rectangles arrording to their coordinates, 
        so that we can know which col and row each color grid belongs to.

        input:
            grids : {
                (x1, y1):color,
                (x1, y1):color,
                (x1, y1):color,
                ...
            }

        output:
            colors in a face, a 3x3 array:[
                [color,color,color],
                [color,color,color],
                [color,color,color]
            ]
    '''

    # sort coordinates by row
    coordinates = sorted(list(grids.keys()), key=lambda x_y: x_y[1])

    if not len(coordinates) == 9:
        # print(coordinates)
        return None

    face = [coordinates[:3], coordinates[3:6], coordinates[6:9]]

    for row in face:

        # sort coordinates inside a row by col
        row.sort(key=lambda x_y: x_y[0])

        # set color to a grid
        for i in range(3):
            row[i] = grids[row[i]]

    return face

# filter {color} in inmage
def hsv_range_mask(image: np.ndarray, _range: tuple) -> np.ndarray:
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower = np.array(_range[0], dtype=np.uint8)
    upper = np.array(_range[1], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower, upper)

    return cv2.bitwise_and(image, image, mask=mask)



def get_colors(image) -> list:

    ''' 
        Get the color of each small grid.

        input:
            image(bgr)

        output:
            colors in a face, a 3x3 array:[
                [color,color,color],
                [color,color,color],
                [color,color,color]
            ]
    '''

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    grids = {}

    for color, (lower, upper) in setting.hsv_ranges.items():
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)

        # get {color} blocks
        color_mask = cv2.inRange(hsv, lower, upper)

        # morphologyEx open: remove noise from the background
        color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_OPEN, open_kernel, iterations=1)

        # morphologyEx close: remove noise from the foreground
        color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_CLOSE, close_kernel, iterations=5)

        # find contours of grids
        cnts, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        rects = straighten(cnts)
        
        for rect in rects:
            grids[rect[0]] = color
            cv2.rectangle(image, rect[0], rect[1], setting.bgr_colors[color], 2)

    result = sort_coordinate(grids)

    return result, image


# test method
def _cube_vision_test():
    
    setting.init()

    image = cv2.imread('tests/in/Cube_3.png')
    face = get_colors(image)
    # print(face)
    cv2.imshow('contours', image)
    cv2.waitKey()


if __name__ == "__main__":

    _cube_vision_test()
