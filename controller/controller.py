import sys
import zmq
import threading
import queue
import socket
import argparse

# Parse command arguments
parser = argparse.ArgumentParser(description='controller')
parser.add_argument('-d', '--dest', required=True, help='manipulator(destination) address (example: 0.0.0.0:10000)')
parser.add_argument('-p', '--port', type=int, default=30000, help='port to listen for new sensors (default: %(default)s)')
args = parser.parse_args()



# Start Subscriber
context = zmq.Context()
sub_socket = context.socket(zmq.SUB)
sub_socket.setsockopt(zmq.SUBSCRIBE, b'')




discover_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
discover_socket.bind(('', args.port))
discover_socket.listen()

def add_sensors(discover_socket, sub_socket): 
    try:
        while True:
            conn, addr = discover_socket.accept()
            try:
                while True:
                    data = conn.recv(128)
                    if not data:
                        break
                    address = str(data, 'utf-8')
                    sub_socket.connect('tcp://' + address)


            finally:
                conn.close()
    finally:
        discover_socket.close()

sensors_thread = threading.Thread(target=add_sensors, args=(discover_socket, sub_socket))
sensors_thread.start()






# Connect to manipulator
dest_ip, dest_port = args.dest.split(':')
send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
send_socket.settimeout(10)
send_socket.connect((dest_ip, int(dest_port)))



import sender
q = queue.Queue()

def worker():
    threading.Timer(5.0, worker).start()
    global q
    sender.proccess_messages(q, send_socket)
    q = queue.Queue()

worker()

try:
    while True:
        message = sub_socket.recv_json()
        q.put(message)
finally:
    sub_socket.close()

send_socket.close()
