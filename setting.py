
L_PADDING = 10

bgr_colors = {
    "gray"   :(128, 128, 128),  # Gray
    "white"  :(128, 128, 128),  # White
    "red"    :(  0,   0, 255),  # Red
    "Red"    :(  0,   0, 255),  # Red
    "green"  :(128, 128, 128),  # Green
    "blue"   :(255,   0,   0),  # Blue
    "yellow" :(  0, 255, 255),  # Yellow
    "orange" :(  0, 165, 255)   # Orange
}

global hsv_range
hsv_range = {
    'Red'   : ([156,  43,  46], [180, 255, 255]), # Red
    'blue'  : ([ 69, 120, 100], [179, 255, 255]), # Blue
    'yellow': ([ 21, 110, 117], [ 45, 255, 255]), # Yellow
    'orange': ([  0, 110, 125], [ 17, 255, 255]), # Orange
    'white' : ([  0,   0, 221], [180,  30, 255]), # White
    'green' : ([ 35,  43,  46], [ 77, 255, 255]), # Green
}

config = 'config.json'

import json

def init():
    try:
        with open(config, 'r') as f:
            cfg = json.loads(f.read())
            
            for color, data in cfg.items():
                hsv_range[color] = (data['lower'], data['upper'])

    except:
        print('something went wrong in', config)


def store():
    data = {}

    for color, (low, up) in hsv_range.items():
        data[color] = {
            'lower':low,
            'upper':up
        }

    with open(config, 'w') as outfile:
        json.dump(data, outfile)