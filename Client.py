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
        print(f"[{client.recv(2048).decode(FORMAT)}] ")
        pozostalo = 100
        #while pozostalo > 0
        input("Time Breake")
        print(send_boat(True,[0,1],1))
        print(send_boat(False,[2,1],2))
        print(send_boat(False,[4,1],3))
        print(send_boat(False,[6,1],3))
        input("Time Breake")
        print(send_boat(False,[8,1],2))
        print(send_boat(True,[2,5],4))
        print(send_boat(False,[8,8],1))
        print(send_boat(False,[0,9],1))
        print(send_boat(False,[6,8],1))
        input("Time Breake")

#orient False dla pionowego   True dla poziomego

def send_boat(orient,pos_start,length):
    client.send(pickle.dumps({"acctiviti":"STATKI","orient":orient,"pos_x":pos_start[0] ,"pos_y":pos_start[1],"length":length}))
    get = client.recv(2048).decode(FORMAT)
    if get == "!DISCONNECT":
        pass
        #break
    print(get)
    if client.recv(2048).decode(FORMAT) == "Wszystkie statki rozstawione":
        return "to już jest koniec"
    else:
        return "Robota czeka"


client.send(pickle.dumps({"acctiviti":"LOGIN","login":"test123","password":"Null"}))
if client.recv(2048).decode(FORMAT) == "True":
    print("zalogowano")
    welcom_menu()
    
else:
    print("Nie udało się zalogować ")