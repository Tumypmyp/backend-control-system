import sys
import socket
import pickle

port = 40000
if len(sys.argv) > 1:
    port = sys.argv[1]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', port))
s.listen()
conn, addr = s.accept()

try:
    while True:
        data = conn.recv(1024)
        if not data:
            break
        message = pickle.loads(data)
        print(message)
finally:
    conn.close()
