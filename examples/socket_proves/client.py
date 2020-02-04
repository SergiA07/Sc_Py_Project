import socket
import threading

def Main1():
    host = '127.0.0.1'
    port1 = 5002
    #port2 = 5004


    mySocket1 = socket.socket()
    #mySocket2 = socket.socket()
    mySocket1.connect((host,port1))
    #mySocket2.connect((host,port2))

    message = input(" ? ")

    while message != 'q':
        mySocket1.send(message.encode())
        data1 = mySocket1.recv(1024).decode()
        #mySocket2.send(message.encode())
        #data2 = mySocket2.recv(1024).decode()

        print('Received1 from server: ' + data1)
        #print('Received2 from server: ' + data2)
        message = input(" ? ")

    mySocket1.close()
    #mySocket2.close()
'''
def Main2():
    host = '127.0.0.1'
    port = 5001

    mySocket = socket.socket()
    mySocket.connect((host,port))

    message = input(" ? ")

    while message != 'q':
        mySocket.send(message.encode())
        data = mySocket.recv(1024).decode()

        print('Received from server: ' + data)
        message = input(" ? ")

    mySocket.close()
'''
if __name__ == '__main__':
    t1 = threading.Thread(target = Main1())
    #t2 = threading.Thread(target = Main2())
    t1.start()
    #t2.start()
