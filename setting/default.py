

bgr_colors = {
    "black"  :(  0,   0,   0),  # Black
    "gray"   :(128, 128, 128),  # Gray
    "white"  :(255, 255, 255),  # White
    "red"    :(  0,   0, 255),  # Red
    "Red"    :(  0,   0, 255),  # Red
    "green"  :(  0, 128,   0),  # Green
    "blue"   :(255,   0,   0),  # Blue
    "yellow" :(  0, 255, 255),  # Yellow
    "orange" :(  0, 165, 255),  # Orange
    "error"  :( 30, 105, 210),  # No matched color, error
}

hsv_ranges = {
    'Red'   : [[156,  43,  46], [180, 255, 255]], # Red
    'red'   : [[  0,  43,  46], [ 13, 255, 255]], # Red
    'blue'  : [[ 69, 120, 100], [179, 255, 255]], # Blue
    'yellow': [[ 21, 110, 117], [ 45, 255, 255]], # Yellow
    'orange': [[  0, 110, 125], [ 17, 255, 255]], # Orange
    'white' : [[  0,   0, 221], [180,  30, 255]], # White
    'green' : [[ 35,  43,  46], [ 77, 255, 255]], # Green
}

# x, y, width: left-top coordinate (x, y) of sample area, (width) of grid
sample = [20, 20, 64]       

hues = [
    ['red'   ,  10],
    ['orange',  25],
    ['yellow',  34],
    ['green' ,  77],
    ['blue'  , 124],
    ['Red'   , 180]
]

saturation = 43

values = [
    ['black',  46],
    ['white', 255]
]

