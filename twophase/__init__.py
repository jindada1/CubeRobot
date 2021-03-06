'''
    kociemba algorithm: twophase approach
    
    solve(cubestring)

    this package is modified from:
        https://github.com/hkociemba/RubiksCube-TwophaseSolver

    original author:
        https://github.com/hkociemba

    package created by kris:
        https://github.com/jindada1
'''

from os import path, mkdir

tables_root = __file__.replace('__init__.py', 'tables')

if not path.exists(tables_root):
    mkdir(tables_root)

def table_path(f):

    return tables_root + '\\' + f

from .solver import solve
