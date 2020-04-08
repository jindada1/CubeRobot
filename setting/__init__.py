'''
setting module:
    manage configuration data
    load config.json in module folder when imported
    store changed value into config.json
'''
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

    # load hues red, orange, yellow, green, blue
    if cfg['hues']:
        hues = cfg['hues']

    # load saturation
    if cfg['saturation']:
        saturation = cfg['saturation']

    # load values for black, white
    if cfg['values']:
        values = cfg['values']
    
    Green = "\x1b[32m"
    End = '\033[0m'
    print(Green + "loading '%s'" % __config_file, End)


def store():

    __configuration['hsv_ranges'] = hsv_ranges
    __configuration['sample'] = sample
    __configuration['saturation'] = saturation
    __configuration['hues'] = hues
    __configuration['values'] = values

    with open(__config_file, 'w') as f:
        json.dump(__configuration, f)
