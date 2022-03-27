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
    client.send(msg)
    print(f"[{client.recv(2048).decode(FORMAT)}] ")

time.sleep(0.5)
Run = True
#print("""
#    WIITAJ
#1 - Zaloguj
#2 - Zarejestruj
#Q - Wyjdź
#""")
while Run:
    inp = input()
    if inp == "Q": 
        send({"acctiviti":DISCONNECT_MESSAGE})
        Run = False
    else:
        send({"acctiviti":"PRINT","content":inp})
