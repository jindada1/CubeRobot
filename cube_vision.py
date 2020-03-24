'''
reference:
    1. Morphological processing
    -> https://blog.csdn.net/sunny2038/article/details/9137759
    -> https://www.jianshu.com/p/dcecaf62da71

    2. color spaces and color segmentation
    -> https://www.learnopencv.com/color-spaces-in-opencv-cpp-python/
    -> https://blog.csdn.net/Taily_Duan/article/details/51506776

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
sample_points = [[] for i in range(9)]
sample_border = [(0, 0),(100, 100)]

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

        left = tuple(cont[:, 0][cont[:, :, 0].argmin()])
        right = tuple(cont[:, 0][cont[:, :, 0].argmax()])
        top = tuple(cont[:, 0][cont[:, :, 1].argmin()])
        bottom = tuple(cont[:, 0][cont[:, :, 1].argmax()])

        # add left-top and right-bottom points
        rects.append(((left[0], top[1]), (right[0], bottom[1])))

    return rects


def sort_coordinate(grids: dict) -> list:
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
            row[i] = grids[row[i]].lower()

    return face


def hsv_range_mask(image: np.ndarray, _range: tuple) -> np.ndarray:
    '''
        filter {color} in inmage
    '''
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower = np.array(_range[0], dtype=np.uint8)
    upper = np.array(_range[1], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower, upper)

    return cv2.bitwise_and(image, image, mask=mask)


def scan_cube(image, mode) -> list:
    ''' 
        Get the color of each small grid.

        input:
            image(bgr)

        output:
            colors in a face, a 3x3 array:[
                [color,color,color],
                [color,color,color],
                [color,color,color]
            ],
            image: modified image
    '''

    if mode == 'm':
        return manual_find(image)

    if mode == 'a':
        return auto_find(image)

def sample_coordinates():

    if not sample_points[0]:
        count_sample_points()
        
    return sample_points


def count_sample_points(new_data=None):

    if new_data:
        setting.sample = new_data

    x, y, w = setting.sample
    
    sample_border[0] = (x, y)
    sample_border[1] = (x + 3*w, y + 3*w)

    # 3 x 3 grids per face
    for i in range(9):
        col, row = i % 3, i // 3
        b_x = col*w + x
        b_y = row*w + y
        '''
            five-point sampling
            x   x
              x
            x   x
        '''
        sample_points[i] = [
            (b_x +   w//4, b_y +   w//4),
            (b_x + 3*w//4, b_y +   w//4),
            (b_x +   w//2, b_y +   w//2),
            (b_x +   w//4, b_y + 3*w//4),
            (b_x + 3*w//4, b_y + 3*w//4)
        ]
    

def get_color(hsv_value):

    h, s, v = hsv_value
    
    if s < setting.s_divide:
        # black, gray, white
        for color, value in setting.v_ranges:
            if v <= value:
                return color

    else:
        # red, orange, yellow, green, blue
        for color, value in setting.h_ranges:
            if h <= value:
                return color
    
    return 'error'

def manual_find(image):
    '''
        we directly specified the sample points for color recognition
    '''
    grid_samples = sample_coordinates()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    face = []

    cv2.rectangle(image, sample_border[0], sample_border[1], (0, 0, 0), 2)
    for points in grid_samples:
        grid_color_candidates = []
        for point in points:
            color = get_color(hsv[point[1], point[0]])
            cv2.circle(image, point, 2, setting.bgr_colors[color] , 2)
            grid_color_candidates.append(color)
        
        # get the most frequent color as the final result
        grid_color = max(set(grid_color_candidates), key = grid_color_candidates.count)
        face.append(grid_color)

    return [face[:3], face[3:6], face[6:9]], image


def auto_find(image):
    '''
        We don't know the position of rubik's cube in image,
        so we try to filter every color and morphologyEx
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

    # setting.init()
    image = cv2.imread('tests/in/Cube_1.png')
    colors, face = scan_cube(image, 'm')
    
    cv2.imshow('contours', image)
    cv2.waitKey()

if __name__ == "__main__":

    _cube_vision_test()
