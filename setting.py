
import json
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

global hsv_ranges
hsv_ranges = {
    'Red'   : ([156,  43,  46], [180, 255, 255]), # Red
    'red'   : ([  0,  43,  46], [ 13, 255, 255]), # Red
    'blue'  : ([ 69, 120, 100], [179, 255, 255]), # Blue
    'yellow': ([ 21, 110, 117], [ 45, 255, 255]), # Yellow
    'orange': ([  0, 110, 125], [ 17, 255, 255]), # Orange
    'white' : ([  0,   0, 221], [180,  30, 255]), # White
    'green' : ([ 35,  43,  46], [ 77, 255, 255]), # Green
}
global sample
sample = [0, 0, 40]
# x, y, width
# left-top coordinate (x, y) of sample area
# width of grid



__config_file = 'config.json'
__config_format = {
    'hsv_ranges': {},
    'h_ranges': {},
    'sample': {}
}

def init():
    try:
        with open(__config_file, 'r') as f:
            cfg = json.loads(f.read())

            # load hsv range of colors
            for color, _range in cfg['hsv_ranges'].items():
                hsv_ranges[color] = (_range['lower'], _range['upper'])

            # load sample points
            if cfg['sample']:
                sample[:] = cfg['sample']

    except:
        print('something went wrong in', config)
    


def store():

    for color, (low, up) in hsv_ranges.items():
        __config_format['hsv_ranges'][color] = {
            'lower': low,
            'upper': up
        }

    __config_format['sample'] = sample

    with open(__config_file, 'w') as outfile:
        json.dump(__config_format, outfile)
