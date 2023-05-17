import socket
import threading
import protocol

def handle_client(client, address, clients):
    global index_msg
    while True:
        try:
            print(len(clients))
            print(index_msg)
            if(len(clients) == 2):
                if(index_msg == 0):
                    # for c in clients:
                    #     print(c)
                    protocol.send_with_size(client, 'OK')
                        # c.sendall('OK'.encode())
                else:
                    # data = client.recv(1024).decode()
                    data = protocol.recv_by_size(client)
                    if not data:
                        break
                    # Forward the message to other clients
                    for c in clients:
                        if c != client:
                            print(f"From {address} data " + data)
                            protocol.send_with_size(c, data)
                            # c.sendall(data.encode())
                index_msg += 1
        except ConnectionResetError:
            print(f'Client {address} disconnected')
            clients.remove(client)
            index_msg = 0
            break
    client.close()


def run_server():
    global index_msg
    host = '0.0.0.0'
    port = 8201
    index_msg = 0

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f'Server is listening on {host}:{port}')

    clients = []

    while True:
        conn, address = server_socket.accept()
        clients.append(conn)
        print(f'New client connected: {address}')

        t = threading.Thread(target=handle_client, args=(conn, address, clients))
        t.start()

if __name__ == '__main__':
    run_server()