import socket
import threading

def Main1():
    host = '127.0.0.1'

    port = 5004


    mySocket = socket.socket()

    mySocket.connect((host,port))

    message = input(" ? ")

    while message != 'q':
        mySocket.send(message.encode())
        data = mySocket.recv(1024).decode()
        print('Received2 from server: ' + data)
        message = input(" ? ")

    mySocket.close()

if __name__ == '__main__':
    t1 = threading.Thread(target = Main1())
    #t2 = threading.Thread(target = Main2())
    t1.start()
    #t2.start()
