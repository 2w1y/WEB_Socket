#from os import pread
import os
import socket
import time
import threading
import sys

HEADER = 64
PORT = 9879
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.56.1"
ADDR = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

time.sleep(0.1)
def chat():
    
    while True:
        user_text = input("Wiadomość do wysłania: ")
        if user_text == "Q":
            break
        send(user_text)
    send(DISCONNECT_MESSAGE)
    

def start():

    thread = threading.Thread(target=chat, args=())
    thread.start()

start()


        