
import json
L_PADDING = 10

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

# global settings in config file
global hsv_ranges, sample, h_ranges, s_divide, v_ranges

hsv_ranges = {
    'Red'   : ([156,  43,  46], [180, 255, 255]), # Red
    'red'   : ([  0,  43,  46], [ 13, 255, 255]), # Red
    'blue'  : ([ 69, 120, 100], [179, 255, 255]), # Blue
    'yellow': ([ 21, 110, 117], [ 45, 255, 255]), # Yellow
    'orange': ([  0, 110, 125], [ 17, 255, 255]), # Orange
    'white' : ([  0,   0, 221], [180,  30, 255]), # White
    'green' : ([ 35,  43,  46], [ 77, 255, 255]), # Green
}

# x, y, width: left-top coordinate (x, y) of sample area, (width) of grid
sample = [20, 20, 64]       

h_ranges = [
    ('red'   ,  10),
    ('orange',  25),
    ('yellow',  34),
    ('green' ,  77),
    ('blue'  , 124),
    ('Red'   , 180)
]

s_divide = 43

v_ranges = [
    ('black',  46),
    ('white', 255)
]


__config_file = 'config.json'
__config_format = {
    'hsv_ranges': {},
    'h_ranges': [],
    's_divide': 43,
    'v_ranges': [],
    'sample': []
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

            # load h ranges red, orange, yellow, green, blue
            if cfg['h_ranges']:
                h_ranges[:] = list(map(lambda l: tuple(l), cfg['h_ranges']))

            # load s divide value
            if cfg['s_divide']:
                s_divide = cfg['s_divide']

            # load v ranges for black, gray, white
            if cfg['v_ranges']:
                v_ranges[:] = list(map(lambda l: tuple(l), cfg['v_ranges']))

    except:
        print('something went wrong in', config)


def store():

    for color, (low, up) in hsv_ranges.items():
        __config_format['hsv_ranges'][color] = {
            'lower': low,
            'upper': up
        }

    __config_format['sample'] = sample
    __config_format['s_divide'] = s_divide

    __config_format['h_ranges'] = list(map(lambda t: list(t), h_ranges))
    __config_format['v_ranges'] = list(map(lambda t: list(t), v_ranges))

    with open(__config_file, 'w') as outfile:
        json.dump(__config_format, outfile)
