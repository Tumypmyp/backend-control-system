# Subscribe to sensors by addreses they sent
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
