from asyncio.windows_events import NULL
from logging import NullHandler
import socket
from sqlite3 import connect 
import threading
import pickle

#Zrobić activiti register

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname("192.168.0.165")
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
user_limit = 32
users = {}
for i in range(user_limit + 1): #AKCeEPTACJA 32 uzytkowników
    users[str(i)] = 0

tables = {}
table_limits = int((user_limit/2) +1)
for i in range(table_limits): #Tworzenie stołów 
    tables[str(i)] = 0


class Table():
    def __init__(self,user):
        self.user_1 = user
        self.user_2 = NULL
        self.full = False
        for table in tables:
            if tables[table] == 0:
                self.id = table 
                self.user_1.conn.send("Table created Succesfull".encode(FORMAT))
                print("[Table created Succesfull]")
                return  
    def join_and_play(self,user):
        self.user_2 = user
        self.full = True
        self.user_2.conn.send("Table joined Succesfull".encode(FORMAT))
        print("[Table joined Succesfull Game Start]")
        self.user_1.conn.send("Gra zaczyna się właśnie teraz User1".encode(FORMAT))
        self.user_2.conn.send("Gra zaczyna się właśnie teraz User2".encode(FORMAT))
        self.user_1.conn.send("Możesz wysłać statki".encode(FORMAT))
        self.user_2.conn.send("Możesz wysłać statki".encode(FORMAT))

    def disconect(self,user):
        print("Disconected from table")
        if self.user_1 == user:
            print("[User1] Disconected from table")
            self.user_2.conn.send("!DISCONNECT".encode(FORMAT))
            self.user_2.connect_game = False
        else:
            print("[User2] Disconected from table")
            self.user_1.conn.send("!DISCONNECT".encode(FORMAT))
            self.user_1.connect_game = False

    def add_boat(self):
        pass
    #Funkcja dodowania łudki do planszy przyjmuje orientacje i punkt zaczynający się statku i statek, Sprawdza czy dany statek może być w danym miejscu 

class Client():
    def __init__(self,conn,addr):
        self.addr = addr
        self.conn = conn
        self.id = NULL
        self.connect_game = True    

    def login(self):
        connected = True
        while connected:
            msg = self.conn.recv(2048)
            try:
                recd = pickle.loads(msg)
            except:
                print("[Użytkownik sie wyjebał na pysk]")
                connected = False
                print("[CONNECTION CLOSED]", self.addr)
                break
            if recd["acctiviti"] == DISCONNECT_MESSAGE:
                connected = False
                print("[CONNECTION CLOSED]", self.addr)
                self.conn.send("Connection succesfull closed :) ".encode(FORMAT))
            if recd["acctiviti"] == "PRINT":
                print(self.addr, self.id, recd["content"])
                self.conn.send("Msg received".encode(FORMAT))
            if recd["acctiviti"] == "LOGIN":
                print(recd["login"])
                print(recd["password"])
                if recd["login"] == "test123":
                    self.conn.send("True".encode(FORMAT))
                    for user in users:
                        if users[user] == 0:
                            self.id = user
                            return True

                else:
                    self.conn.send("False".encode(FORMAT))
            
        self.conn.close()
        return False


    def waitning(self):
        print("[Wainting]", self.addr)
        connected = True
        while connected:
            msg = self.conn.recv(2048)
            try:
                recd = pickle.loads(msg)
            except:
                print("[Użytkownik sie wyjebał na pysk]")
                connected = False
                print("[CONNECTION CLOSED]", self.addr)
                self.conn.close()
                users[self.id] = 0
                self.connect_game = False
                break
            if recd["acctiviti"] == "TABLE":
                for table in tables:
                    if tables[table] != 0:
                        if tables[table].full == False:
                            tables[table].join_and_play(users[self.id])
                            self.table = tables[table]
                            connected = False
                            print("breake", self.addr)
                            break
                    else:
                        tablee = Table(users[self.id])
                        tables[tablee.id] = tablee
                        self.table = tablee
                        connected = False
                        print("breake", self.addr)
                        break
    def game(self):
        print("[Game Start]", self.addr)
        self.connect_game = True
        while self.connect_game:
            msg = self.conn.recv(2048)
            recd = pickle.loads(msg)
            

            if recd["acctiviti"] == "MESSAGE":
                print(f"[Table id {self.table.id}] Message: " + recd['CONTENT'] ) #Message beetwen 2 users
                if self.table.user_1.id == self.id:
                    print("tu")
                    self.table.user_2.conn.send(recd["CONTENT"].encode(FORMAT))
                else:
                    print("tam")
                    self.table.user_1.conn.send(recd["CONTENT"].encode(FORMAT))
            if recd["acctiviti"] == "!DISCONNECT":
                print("[]Użytkownik rozłączył sie podczas stołu")
                self.table.disconect(users[self.id])
                self.connect_game = False ###Zamykanie instancji stołu
        print("[]Gra zakończona prawidłowo")

def handle_client(conn, addr):
    global users
    print(f"[NEW CONNECTION] {addr} connected.")
    print("[USER ADD]", addr)
    guest =  Client(conn,addr)
    status = guest.login()
    print("status", status)
    if status:
        print("[AUTHENTICATION SUCCESFULL] id:", guest.id)
        users[guest.id] = guest
        status = guest.waitning()
        while guest.connect_game:
            guest.game()
            
            guest.waitning()
    else:
        print("[AUTHENTICATION FALS]")


def start():
    server.listen(32)
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()