# Subscribe to sensors by addreses they sent
def add_sensors(discover_socket, sub_socket): 
    print('adding sensors')
    try:
        while True:
            conn, addr = discover_socket.accept()
            print('connecting to ', addr)
            try:
                data = conn.recv(128)
                if not data:
                    break
                address = str(data, 'utf-8')
                sub_socket.connect('tcp://' + address)
            finally:
                conn.close()
        print('discoverer closed')
    finally:
        discover_socket.close()
