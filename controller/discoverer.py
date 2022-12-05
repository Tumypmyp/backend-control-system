import socket

def discover_sensors(port, sub_socket):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen()
    add_sensors(s, sub_socket)

# Subscribe to sensors by addreses they sent
def add_sensors(discover_socket, sub_socket): 
    try:
        while True:
            conn, addr = discover_socket.accept()
            try:
                # Get address of sensor's publisher
                data = conn.recv(128)
                if not data:
                    break
                address = str(data, 'utf-8')
                sub_socket.connect('tcp://' + address)
            finally:
                conn.close()
    finally:
        discover_socket.close()
