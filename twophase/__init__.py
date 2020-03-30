
tables_root = __file__.replace('__init__.py', 'tables')

def table_path(f):

    return tables_root + '\\' + f

from .solver import solve
