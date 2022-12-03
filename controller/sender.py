import pickle
from datetime import datetime


def proccess_messages(queue, socket):
    sum = 0
    size = 0
    while not queue.empty():
        m = queue.get()
        sum += m['payload']
        size += 1
    print(f'Number of messages: {size}, Sum of payloads: {sum}')
    send_status(socket, 'up' if sum % 2 == 0 else 'down')


def send_status(socket, status):
    dt = datetime.now().strftime('%Y%m%dT%H%M')
    result = {'datetime': dt, 'Status': status}
    socket.sendall(pickle.dumps(result))
