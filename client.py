import socket
import protocol

c_sock = socket.socket()
c_sock.connect(('192.168.1.32',8201))
print('connect sucsesfully!')
p = False
check_first_msg = False
c_sock.settimeout(2)

while not check_first_msg:
    try:
        # data = c_sock.recv(1024).decode()
        data = protocol.recv_by_size(c_sock)
        print(data)
        if ('OK' in data):
            check_first_msg = True
            break
    except:
        pass
print('start')

while True:
    try:
        message = input("input: ")
        # c_sock.sendall(message.encode())
        protocol.send_with_size(c_sock, message)

        data = protocol.recv_by_size(c_sock)
        # data = c_sock.recv(1024).decode()
        if data:
            print(data)

    except:
        pass

c_sock.close()