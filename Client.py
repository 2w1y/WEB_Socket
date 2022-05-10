import socket
import time
import pickle
import threading
import sys


PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.0.165"
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
#while Run:
#    inp = input()
#    if inp == "Q": 
#        send({"acctiviti":DISCONNECT_MESSAGE})
#        Run = False
#    else:
#        send({"acctiviti":"PRINT","content":inp})


def leesen():
    while True:
        get = client.recv(2048).decode(FORMAT)
        if get == "!DISCONNECT":
            break
        print(f"[{get}]")
        print("Wysyyłanie wiadomości do innego uzytkownika: ")

def welcom_menu():
    x = input("Podaj 1:")
    if x == "1":
        send({"acctiviti":"TABLE"})
        print(f"[{client.recv(2048).decode(FORMAT)}] ") #dodać ewentualny except od strony serwera jeśli coś wywali się na tym etapie
        thread = threading.Thread(target=leesen)
        thread.start()
        y = True
        while y:
            inp = input("Wysyyłanie wiadomości do innego uzytkownika: ")
            if inp == "Q":
                client.send(pickle.dumps({"acctiviti":DISCONNECT_MESSAGE}))
                y = False
                thread.stop()
                sys.exit()
            else:
                client.send(pickle.dumps({"acctiviti":"MESSAGE","CONTENT":inp}))



client.send(pickle.dumps({"acctiviti":"LOGIN","login":"test123","password":"Null"}))
if client.recv(2048).decode(FORMAT) == "True":
    print("zalogowano")
    welcom_menu()
else:
    print("Nie udało się zalogować ")