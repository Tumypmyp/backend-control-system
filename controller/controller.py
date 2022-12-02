import sys
import zmq
import threading
import queue

port = '5556'
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

if len(sys.argv) > 2:
    port1 =  sys.argv[2]
    int(port1)

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print('Collecting updates from weather server...')
socket.connect(f'tcp://localhost:{port}')

if len(sys.argv) > 2:
    socket.connect(f'tcp://localhost:{port1}')

socket.setsockopt(zmq.SUBSCRIBE, b'')


q = queue.Queue()

def use_messages(q):
    sum = 0
    size = 0
    while not q.empty():
        m = q.get()
        sum += m['payload']
        size += 1
    print('Result:', sum, size)



def worker():
    threading.Timer(5.0, worker).start()
    global q
    use_messages(q)
    q = queue.Queue()

worker()

while True:
    message = socket.recv_json()
    print(message)
    q.put(message)
