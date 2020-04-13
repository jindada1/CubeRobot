'''
start or stop a http server in a thread
you can add more routes you like and respond with text/html/json etc
'''
import socket
from threading import Thread

global RUNNING
RUNNING = True

def get_request(b_header):
    header_str = b_header.decode().lower()
    req = (header_str.split('\r\n'))[0]
    return req.split(' ')

def text_response(text):
    http_reply = 'HTTP/1.x 200 ok\r\nContent-Type: text/plain\r\nAccess-Control-Allow-Origin: *\r\n\r\n'
    http_reply += text
    return http_reply.encode()

def module_path(html_name='index.html'):
    
    folder = __file__[:__file__.rfind('\\')]
    h_file = '%s\\%s' % (folder, html_name)

    return h_file


def index():
    html = 'HTTP/1.x 200 ok\r\nContent-Type: text/html\r\n\r\n'

    with open(module_path('emulator.html'), mode='r', encoding='utf8') as text:
        html += text.read()
    
    return html.encode('gbk')
    

def router(route):
    
    if route[:7] == '/solve/':
        cube = route[7:]
        seq = solve(cube)
        return text_response(seq)

    elif route[:5] == '/stop':
        stop_http_server()
        return text_response('server stopped')
    
    elif route == '/':
        return index()

    return text_response('error')


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
    
    try:
        from twophase import solve
    except:
        print('未加载 twophase 模块')

    port = 8888
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind(('', port))
    except socket.error as e:
        print('Server socket bind failed. Error Code : ' + str(e.errno))
        sys.exit()
        
    s.listen(10)
    print('-------------------------------------')
    print('Server run in http://127.0.0.1:%d' % port)

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
    
    start_http_server()