'''
contains two submodules: http server and socket client

http server:
    start or stop a http server in a thread
    you can add more routes you like and respond with text/html/json etc

socket client:
    connect to host
    receive msg from host
    send msg to host
    disconnect from host
'''
from .http_server import start_http_server, stop_http_server
from .sock_client import SClient

__all__ = [
    'start_http_server',
    'stop_http_server',
    'SClient'
]

__version__ = '1.0'
__author__ = 'Kris Huang'
