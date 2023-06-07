SIZE_LENGTH_BYTES = 8
TCP_DEBUG = True

def recv_by_size(sock, return_type="string"):
    sock.settimeout(0.001)
    str_size = b""
    data_len = 0
    while len(str_size) < SIZE_LENGTH_BYTES:
        _d = sock.recv(SIZE_LENGTH_BYTES - len(str_size))
        if len(_d) == 0:
            str_size = b""
            break
        str_size += _d
    data = b""
    str_size = str_size.decode('ISO-8859-1')
    if str_size != "":
        data_len = int(str_size[:SIZE_LENGTH_BYTES - 1])
        while len(data) < data_len:
            _d = sock.recv(data_len - len(data))
            if len(_d) == 0:
                data = b""
                break
            data += _d
    if TCP_DEBUG and len(str_size) > 0:
        data_to_print = data[:]
        if type(data_to_print) == bytes:
            try:
                data_to_print = data_to_print.decode('ISO-8859-1')
            except (UnicodeDecodeError, AttributeError):
                pass
        # print(f"\nReceive({str_size})>>>{data_to_print}")

    if data_len != len(data):
        data=b"" # Partial data is like no data !
    if return_type == "string":
        return data.decode('ISO-8859-1')
    return data


def send_with_size(sock, data):
    sock.settimeout(0.001)
    len_data = str(len(data)).zfill(SIZE_LENGTH_BYTES - 1) + "|"
    len_data = len_data.encode('ISO-8859-1')
    if type(data) != bytes:
        data = data.encode('ISO-8859-1')
    data = len_data + data
    sock.send(data)
    # print('send: ' + data.decode())

    if TCP_DEBUG and len(len_data) > 0:
        data = data[:]
        if type(data) == bytes:
            try:
                data = data.decode('ISO-8859-1')
            except (UnicodeDecodeError, AttributeError):
                pass
        # print(f"\nSent({len_data})>>>{data}")
