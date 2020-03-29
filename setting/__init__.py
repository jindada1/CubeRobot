from .default import *
import json

__config_file = __file__.replace('__init__.py', 'config.json')

__configuration = {}

with open(__config_file, 'r') as f:
    cfg = json.loads(f.read())

    # load hsv range of colors
    if cfg['hsv_ranges']:
        hsv_ranges = cfg['hsv_ranges']

    # load sample points
    if cfg['sample']:
        sample = cfg['sample']

    # load h ranges red, orange, yellow, green, blue
    if cfg['hues']:
        hues = cfg['hues']

    # load s divide value
    if cfg['saturation']:
        saturation = cfg['saturation']

    # load v ranges for black, gray, white
    if cfg['values']:
        values = cfg['values']
    
    print('load from %s' % __config_file)


def store():

    __configuration['hsv_ranges'] = hsv_ranges
    __configuration['sample'] = sample
    __configuration['saturation'] = saturation
    __configuration['hues'] = hues
    __configuration['values'] = values

    with open(__config_file, 'w') as f:
        json.dump(__configuration, f)
