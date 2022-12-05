import pickle
from datetime import datetime

# Count messages and sent the control signal
def proccess_messages(queue, socket, status):
    sum = 0
    size = 0
    while not queue.empty():
        m = queue.get()
        sum += m['payload']
        size += 1
    print(f'Number of messages: {size}, Sum of payloads: {sum}')
    send_status(socket, 'up' if sum % 2 == 0 else 'down', status)


# send the control signal
def send_status(socket, status, server_status):
    dt = datetime.now().strftime('%Y%m%dT%H%M')
    result = {'datetime': dt, 'Status': status}
    server_status['datetime'] = dt
    server_status['Status'] = status
    socket.sendall(pickle.dumps(result))
