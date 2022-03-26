from re import X
import socket
import time
import pickle



PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.56.1"
ADDR = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    msg = pickle.dumps(msg)
    print(msg)
    client.send(msg)
    print(client.recv(2048).decode(FORMAT))

time.sleep(0.5)
x = {"acctiviti":"HI"}
send(x)
x = {"acctiviti":DISCONNECT_MESSAGE}
send(x)