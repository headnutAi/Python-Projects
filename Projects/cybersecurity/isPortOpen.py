import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = ("127.0.0.1", 8080)

result = sock.connect_ex(addr)


if result == 0:
    print("port open")
    sock.close()
else:
    print("port closed")