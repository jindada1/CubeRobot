'''
start or stop a http server in a thread
you can add more routes you like and respond with text/html/json etc
'''
import socket
from threading import Thread
from twophase import solve

global RUNNING
RUNNING = True

def get_request(b_header):
    header_str = b_header.decode().lower()
    req = (header_str.split('\r\n'))[0]
    return req.split(' ')


def router(route):
    http_reply = 'HTTP/1.x 200 ok\r\nContent-Type: text/plain\r\nAccess-Control-Allow-Origin: *\r\n\r\n'

    if route[:7] == '/solve/':
        cube = route[7:]
        http_reply += solve(cube)

    elif route[:6] == '/stop/':
        stop_http_server()

    return http_reply.encode()


def http_handler(conn):
    b_header = conn.recv(1024)

    if not b_header:
        return
        
    req = get_request(b_header)
    if len(req) != 3:
        return
    
    method, route, proto = req

    resp = router(route)
    conn.sendall(resp)


def start_http_server(handler=http_handler):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        s.bind(('', 8888))
    except socket.error as e:
        print('Server socket bind failed. Error Code : ' + str(e.errno))
        sys.exit()
        
    s.listen(10)
    print('Server listening...')

    while RUNNING:
        try:
            conn, addr = s.accept()
            print('[Connected] with %s:%d'% (addr[0], addr[1]))
            Thread(target=handler, args=(conn,)).start()

        except:
            print('Error')

    print('Server stopped')
    s.close()


def stop_http_server():
    global RUNNING
    RUNNING = False


if __name__ == "__main__":
    
    start_server()
