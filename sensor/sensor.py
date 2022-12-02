import zmq
import random
import sys
import time
from datetime import datetime

port = '5556'
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
pub_socket = context.socket(zmq.PUB)
pub_socket.bind(f'tcp://*:{port}')

try:
    while True:
        dt = datetime.now().strftime('%Y%m%dT%H%M')
        payload = random.randrange(1, 200)
        data = {'datetime' : dt, 'payload' : payload}
        print(data)

        pub_socket.send_json(data)
        time.sleep(1)
finally:
    pub_socket.close()
