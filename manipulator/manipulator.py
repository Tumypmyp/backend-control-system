import sys
import socket
import pickle
import argparse

# Parse command arguments
parser = argparse.ArgumentParser(description='Proccess messages got from the controller')
parser.add_argument('-p', '--port', type=int, default=10000, help='port to listen the tcp connection (default: %(default)s)')
args = parser.parse_args()
print(args)

# Start TCP server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', args.port))
s.listen()

try:
    while True:
        # Listen for connections
        conn, addr = s.accept()
        try:
            while True:
                # Load updates
                data = conn.recv(64)
                if not data:
                    break
                message = pickle.loads(data)
                print(message)
        finally:
            conn.close()
finally:
    s.close()
