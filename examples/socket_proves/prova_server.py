# Two servers are created on at the same time with multi-threading!
import socket
import time
import threading


def Main1():
    print("1")
    host = "127.0.0.1"
    port = 5002

    mySocket = socket.socket()
    mySocket.bind((host, port))

    mySocket.listen(1)
    conn, addr = mySocket.accept()
    print("Connection from: " + str(addr))

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("from connected user: " + str(addr))

        data = str(data).upper()
        print("Received from User: " + str(data))

        # data = input(" ? ")
        response_to_client = "hi this is server1 echo: I received " + str(data)
        conn.send(response_to_client.encode())

    conn.close()


def Main2():
    print("2")
    host = "127.0.0.1"
    port = 5004

    mySocket = socket.socket()
    mySocket.bind((host, port))

    mySocket.listen(1)
    conn, addr = mySocket.accept()
    print("Connection from: " + str(addr))

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("from connected User: " + str(addr))

        data = str(data).upper()
        print("Received from User: " + str(data))

        # data = input(" ? ")
        response_to_client = "hi this is server2 echo: I received " + str(data)
        conn.send(response_to_client.encode())

    conn.close()


if __name__ == '__main__':
    t1 = threading.Thread(target=Main1)
    t2 = threading.Thread(target=Main2)
    t1.start()
    t2.start()
    print("done")
