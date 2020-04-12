
# bgr_colors = { color: (b, g, r), }
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

# hsv_ranges = { color: [hsv_lower, hsv_upper], }
hsv_ranges = {
    'Red'   : [[156,  43,  46], [180, 255, 255]], # Red
    'red'   : [[  0,  43,  46], [ 13, 255, 255]], # Red
    'blue'  : [[ 69, 120, 100], [179, 255, 255]], # Blue
    'yellow': [[ 21, 110, 117], [ 45, 255, 255]], # Yellow
    'orange': [[  0, 110, 125], [ 17, 255, 255]], # Orange
    'white' : [[  0,   0, 221], [180,  30, 255]], # White
    'green' : [[ 35,  43,  46], [ 77, 255, 255]], # Green
}

'''
    x, y, w: left-top coordinate (x, y) of sample area, (width) of grid

    (0,0)
        +-x-|
        |   |
        y   |
        |   |     |--w--|  
        ----+-----+-----+-----+
            |     |     |     |
            +-----+-----+-----+
            |     |     |     |
            +-----+-----+-----+
            |     |     |     |
            +-----+-----+-----+
            sample area
'''
sample = [20, 20, 64]


'''
    if s < saturation:
        color must belongs to [black, gray, white]
        search in values
    else:
        color belongs to [red, orange, yellow, green, blue, Red]
        search in hues
'''
saturation = 43

'''
    if 0 <= hue < 3, color is red
    elif 3 <= hue < 18, color is orange
    ...
'''
hues = [
    ['red'   ,   3],
    ['orange',  18],
    ['yellow',  50],
    ['green' ,  77],
    ['blue'  , 124],
    ['Red'   , 181]
]

'''
    if 0 <= value < 0, color is black
    elif 0 <= value < 0, color is gray
    elif 0 <= value < 256, color is white
    common rubik's cube does not have black or gray grid, so we set black and gray to 0
    ...
'''
values = [
    ['black',   0],
    ['gray',    0],
    ['white', 256]
]

'''
wifi configuration: [ssid, password]
'''
wifi = ['Rubik-Cube', '1213141516']