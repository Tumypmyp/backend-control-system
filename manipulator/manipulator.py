import sys
import socket
import pickle
import argparse

parser = argparse.ArgumentParser(description='Proccess messages got from the controller')
parser.add_argument('-p', '--port', type=int, default=10000, help='port to listen the tcp connection (default: %(default)s)')
args = parser.parse_args()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', args.port))
s.listen()
conn, addr = s.accept()

try:
    while True:
        data = conn.recv(64)
        if not data:
            break
        message = pickle.loads(data)
        print(message)
finally:
    conn.close()
